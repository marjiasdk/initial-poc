import os
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

# Load the flawed dataset
df = pd.read_csv("../data/flawed_dataset.csv")

# 1. Language Bias Detection with Cerebras Inference
@lru_cache(maxsize=1000)
def detect_language_bias_with_inference(text):
    retries = 3
    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                messages=[{
                    "role": "system",
                    "content": (
                        "You are a bias detection assistant. Analyze the following message for biased or stereotypical language, "
                        "such as terms that might reflect gender, racial, or personality-based stereotypes. "
                        "If you detect any biased language, respond with 'contains bias', otherwise respond with 'no bias'."
                    )
                }, {"role": "user", "content": text}],
                model="llama3.1-8b",
                max_completion_tokens=20,
                temperature=0.2
            )
            content = response.choices[0].message.content.strip().lower()
            return "contains bias" in content
        except InternalServerError:
            if attempt < retries - 1:
                logging.warning(f"Attempt {attempt + 1} failed. Retrying...")
                time.sleep(2)
            else:
                logging.error(f"Failed to process message after {retries} attempts: {text}")
                return False

df['language_bias_flag'] = df['customer_message'].apply(
    lambda msg: detect_language_bias_with_inference(msg) if pd.notnull(msg) else False
)
print("Language bias detected in entries:")
print(df[df['language_bias_flag']])

# 2. Demographic Bias Detection (Gender Representation) with Cerebras Inference
@lru_cache(maxsize=1000)
def detect_gender_bias_with_inference(name):
    retries = 3
    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                messages=[{
                    "role": "system",
                    "content": (
                        "You are a demographic analysis assistant. Analyze the following name and determine if it has a gender association. "
                        "If the name is commonly associated with a male gender, respond with 'male'; if with a female gender, respond with 'female'. "
                        "If the name is gender-neutral or unrecognized, respond with 'unknown'."
                    )
                }, {"role": "user", "content": name}],
                model="llama3.1-8b",
                max_completion_tokens=20,
                temperature=0.2
            )
            content = response.choices[0].message.content.strip().lower()
            if "male" in content:
                return "male"
            elif "female" in content:
                return "female"
            else:
                return "unknown"
        except InternalServerError:
            if attempt < retries - 1:
                logging.warning(f"Attempt {attempt + 1} failed. Retrying...")
                time.sleep(2)
            else:
                logging.error(f"Failed to process name after {retries} attempts: {name}")
                return "unknown"

df['gender_bias_flag'] = df['name'].apply(
    lambda name: detect_gender_bias_with_inference(name) if pd.notnull(name) else "unknown"
)
print("\nGender representation in dataset:")
print(df['gender_bias_flag'].value_counts())

# Generate Bias Summary
language_bias_count = df['language_bias_flag'].sum()
gender_bias_summary = df['gender_bias_flag'].value_counts()

print("\nBias Summary:")
print(f"Language Bias Count: {language_bias_count}")
print("Gender Bias Representation:")
print(gender_bias_summary)
