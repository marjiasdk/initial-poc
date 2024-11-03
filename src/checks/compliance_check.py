import os
import re
import time
import pandas as pd
from cerebras.cloud.sdk import Cerebras, InternalServerError
from dotenv import load_dotenv
from functools import lru_cache
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO)

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("CEREBRAS_API_KEY")
if not api_key:
    raise ValueError("API Key not found. Please set the CEREBRAS_API_KEY in your .env file.")

client = Cerebras(api_key=api_key)

# Load the dataset
df = pd.read_csv("../data/flawed_dataset.csv")

# Compliance checks using regex for different types of PII
def detect_email(text):
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    return bool(re.search(email_pattern, str(text)))

def detect_ssn(text):
    ssn_pattern = r'\b\d{3}-\d{2}-\d{4}\b'
    return bool(re.search(ssn_pattern, str(text)))

def detect_phone(text):
    phone_pattern = r'\b\d{3}-\d{4}\b|\b\d{3}-\d{3}-\d{4}\b'
    return bool(re.search(phone_pattern, str(text)))

# Inference-based PII detection
@lru_cache(maxsize=1000)  # Caching to avoid redundant API calls for similar text
def check_pii_with_inference(text):
    retries = 3
    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                messages=[{
                    "role": "system",
                    "content": (
                        "You are a compliance officer. Analyze the following message to determine if it contains personally identifiable information (PII), "
                        "such as an email address, Social Security number (SSN), or phone number. Respond with 'contains pii' if any PII is found, otherwise respond with 'no pii'."
                    )
                }, {"role": "user", "content": text}],
                model="llama3.1-8b",
                max_completion_tokens=20,
                temperature=0.2
            )
            content = response.choices[0].message.content.strip().lower()
            return "contains pii" in content
        except InternalServerError:
            if attempt < retries - 1:
                logging.warning(f"Attempt {attempt + 1} failed. Retrying...")
                time.sleep(5)
            else:
                logging.error(f"Failed to process message after {retries} attempts: {text}")
                return False

# Apply compliance checks
df['email_flag'] = df['customer_message'].apply(detect_email) | df['contact_info'].apply(detect_email)
df['ssn_flag'] = df['customer_message'].apply(detect_ssn) | df['contact_info'].apply(detect_ssn)
df['phone_flag'] = df['customer_message'].apply(detect_phone) | df['contact_info'].apply(detect_phone)
df['pii_flag_inference'] = df['customer_message'].apply(lambda msg: check_pii_with_inference(msg) if pd.notnull(msg) else False)

# Combine flags
df['pii_flag'] = df['email_flag'] | df['ssn_flag'] | df['phone_flag'] | df['pii_flag_inference']

# Optional: Detailed PII flag
def get_pii_details(row):
    details = []
    if row['email_flag']: details.append("email")
    if row['ssn_flag']: details.append("ssn")
    if row['phone_flag']: details.append("phone")
    if row['pii_flag_inference']: details.append("inferred pii")
    return ", ".join(details) if details else "no pii"

df['pii_flag_details'] = df.apply(get_pii_details, axis=1)

# Display the results
print(df[['customer_message', 'contact_info', 'email_flag', 'ssn_flag', 'phone_flag', 'pii_flag_inference', 'pii_flag', 'pii_flag_details']])
