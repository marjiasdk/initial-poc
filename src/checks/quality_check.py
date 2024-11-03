import os
import re
import time
import pandas as pd
from cerebras.cloud.sdk import Cerebras, InternalServerError
from dotenv import load_dotenv
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO)

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("CEREBRAS_API_KEY")
if not api_key:
    raise ValueError("API Key not found. Please set the CEREBRAS_API_KEY in your .env file.")

# Initialize the Cerebras client with the loaded API key
client = Cerebras(api_key=api_key)

# Load the CSV file
df = pd.read_csv("../data/flawed_dataset.csv")

# 1. Relevance Check with Cerebras Inference
def check_relevance(message):
    """Determines if a message is relevant for customer support purposes using Cerebras API."""
    retries = 3
    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                messages=[{
                    "role": "system",
                    "content": (
                        "You are a classifier for customer support messages. "
                        "Classify a customer message as 'relevant' if it includes inquiries about orders, complaints, product questions, cancellations, or account support. "
                        "If the message is unrelated to customer support, random, or contains sensitive information without a request for support, classify it as 'irrelevant'."
                    )
                }, {"role": "user", "content": message}],
                model="llama3.1-8b",
                max_completion_tokens=50,
                temperature=0.2
            )
            content = response.choices[0].message.content.strip()
            is_relevant = "relevant" in content.lower()

            # Additional checks for sensitive and irrelevant content
            sensitive_terms = ["ssn", "social security", "phone number", "email"]
            irrelevant_phrases = ["random", "no purpose", "unrelated", "placeholder"]

            if any(term in message.lower() for term in sensitive_terms):
                return False
            if any(phrase in message.lower() for phrase in irrelevant_phrases):
                return False

            return is_relevant
        except InternalServerError:
            if attempt < retries - 1:
                logging.warning(f"Attempt {attempt + 1} failed. Retrying...")
                time.sleep(2)
            else:
                logging.error(f"Failed to process message after {retries} attempts: {message}")
                return None

def check_relevance_with_delay(message):
    """Wrapper to add delay between relevance checks to avoid rate limits."""
    time.sleep(0.2)  # Adjust as needed based on rate limits
    return check_relevance(message)

df['relevance_flag'] = df['customer_message'].apply(
    lambda msg: check_relevance_with_delay(msg) if pd.notnull(msg) else None
)

# 2. Duplicate Detection
df['duplicate_flag'] = df.duplicated(subset=['customer_message'], keep=False)

# 3. Completeness Check for Essential Fields
df['missing_message'] = df['customer_message'].isnull()
df['missing_name'] = df['name'].isnull()

# 4. Language Quality Check
def detect_language_quality(text):
    """Checks for poor language quality, such as incomplete sentences or excessive special characters."""
    if pd.isnull(text):
        return False
    poor_quality_pattern = r'[^A-Za-z0-9\s.,!?\'"-]{3,}|^\W+|\W+$|[A-Za-z]{1}\s+[A-Za-z]{1}'
    return bool(re.search(poor_quality_pattern, text))

df['language_quality_flag'] = df['customer_message'].apply(detect_language_quality)

# Save results to a new CSV file
df.to_csv("../data/evaluated_dataset.csv", index=False)

# Display the DataFrame with all quality flags
print(df[['customer_message', 'relevance_flag', 'duplicate_flag', 'missing_message', 'missing_name', 'language_quality_flag']])
