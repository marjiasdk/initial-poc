import pandas as pd

def generate_report(df, output_path="../data/report.txt"):
    with open(output_path, "w") as file:
        file.write("Dataset Quality and Compliance Report\n")
        file.write("=" * 40 + "\n\n")

        # Data Quality Summary
        file.write("1. Data Quality Summary\n")
        file.write("-" * 40 + "\n")
        
        # Relevance check
        if 'relevance_flag' in df.columns:
            relevance_count = df['relevance_flag'].value_counts().to_dict()
            file.write(f"Relevant Entries: {relevance_count.get(True, 0)}\n")
            file.write(f"Irrelevant Entries: {relevance_count.get(False, 0)}\n")
        else:
            file.write("Relevance Check Not Performed\n")
        
        # Duplicates
        if 'duplicate_flag' in df.columns:
            duplicates_count = df['duplicate_flag'].sum()
            file.write(f"Duplicate Entries: {duplicates_count}\n")
        else:
            file.write("Duplicate Check Not Performed\n")

        # Completeness
        if 'missing_message' in df.columns:
            missing_message_count = df['missing_message'].sum()
            file.write(f"Entries with Missing Messages: {missing_message_count}\n")
        else:
            file.write("Missing Message Check Not Performed\n")
        
        if 'missing_name' in df.columns:
            missing_name_count = df['missing_name'].sum()
            file.write(f"Entries with Missing Names: {missing_name_count}\n")
        else:
            file.write("Missing Name Check Not Performed\n")

        # Language Quality
        if 'language_quality_flag' in df.columns:
            language_quality_count = df['language_quality_flag'].sum()
            file.write(f"Entries with Poor Language Quality: {language_quality_count}\n\n")
        else:
            file.write("Language Quality Check Not Performed\n\n")

        # Compliance Summary
        file.write("2. Compliance Summary\n")
        file.write("-" * 40 + "\n")
        if 'email_flag' in df.columns:
            pii_email_count = df['email_flag'].sum()
            file.write(f"Entries with Detected Email PII: {pii_email_count}\n")
        else:
            file.write("Email PII Detection Not Performed\n")

        if 'ssn_flag' in df.columns:
            pii_ssn_count = df['ssn_flag'].sum()
            file.write(f"Entries with Detected SSN PII: {pii_ssn_count}\n")
        else:
            file.write("SSN PII Detection Not Performed\n")

        if 'phone_flag' in df.columns:
            pii_phone_count = df['phone_flag'].sum()
            file.write(f"Entries with Detected Phone PII: {pii_phone_count}\n")
        else:
            file.write("Phone PII Detection Not Performed\n")

        pii_total_count = (
            df['email_flag'].sum() if 'email_flag' in df.columns else 0
        ) + (
            df['ssn_flag'].sum() if 'ssn_flag' in df.columns else 0
        ) + (
            df['phone_flag'].sum() if 'phone_flag' in df.columns else 0
        )
        file.write(f"Total Entries with PII: {pii_total_count}\n\n")

        # Summary Statistics
        file.write("4. Summary Statistics\n")
        file.write("-" * 40 + "\n")
        total_entries = len(df)
        quality_issues = sum([
            df['relevance_flag'].value_counts().get(False, 0) if 'relevance_flag' in df.columns else 0,
            df['duplicate_flag'].sum() if 'duplicate_flag' in df.columns else 0,
            df['missing_message'].sum() if 'missing_message' in df.columns else 0,
            df['missing_name'].sum() if 'missing_name' in df.columns else 0,
            df['language_quality_flag'].sum() if 'language_quality_flag' in df.columns else 0,
        ])
        compliance_issues = pii_total_count

        file.write(f"Total Entries in Dataset: {total_entries}\n")
        file.write(f"Entries with Quality Issues: {quality_issues}\n")
        file.write(f"Entries with Compliance Issues: {compliance_issues}\n\n")

        file.write("Note: This report provides a summary of detected quality, compliance, and bias issues in the dataset.\n")

    print(f"Report generated and saved to {output_path}")
