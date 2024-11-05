import os
import re
import time
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from cerebras.cloud.sdk import Cerebras, InternalServerError
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("CEREBRAS_API_KEY")
if not api_key:
    raise ValueError("API Key not found. Please set the CEREBRAS_API_KEY in your .env file.")
client = Cerebras(api_key=api_key)

# Import specific functions as needed
from checks.quality_check import check_relevance
from checks.compliance_check import detect_email, detect_ssn, detect_phone
from checks.bias_check import detect_language_bias_with_inference, detect_gender_bias_with_inference
from report_generator import generate_report

st.title("Evadence: Ensuring Quality, Compliance, and Ethical Standards for AI Training Data")

# File upload
uploaded_file = st.file_uploader("Upload your dataset (CSV format)", type="csv")

# Analysis options
relevance_check = st.checkbox("Run Relevance Check")
pii_detection = st.checkbox("Run PII Detection")
bias_detection = st.checkbox("Run Bias Detection")

# Run analysis when button is clicked
if st.button("Run Analysis"):
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        total_entries = len(df)

        # Initialize checks based on enabled options
        if relevance_check:
            df['relevance_flag'] = df['customer_message'].apply(lambda x: check_relevance(x) if pd.notnull(x) else None)

        df['duplicate_flag'] = df.duplicated(subset=['customer_message'], keep=False)
        df['missing_message'] = df['customer_message'].isnull()
        df['missing_name'] = df['name'].isnull()

        # Language Quality Check
        def detect_language_quality(text):
            poor_quality_pattern = r'[^A-Za-z0-9\s.,!?\'"-]{3,}|^\W+|\W+$|[A-Za-z]{1}\s+[A-Za-z]{1}'
            return bool(re.search(poor_quality_pattern, str(text)))
        df['language_quality_flag'] = df['customer_message'].apply(detect_language_quality)

        # PII Detection
        if pii_detection:
            for flag, func in {'email_flag': detect_email, 'ssn_flag': detect_ssn, 'phone_flag': detect_phone}.items():
                df[flag] = df['customer_message'].apply(func) | df['contact_info'].apply(func)

        # Bias Detection
        if bias_detection:
            df['language_bias_flag'] = df['customer_message'].apply(
                lambda msg: detect_language_bias_with_inference(msg) if pd.notnull(msg) else False
            )
            df['gender_bias_flag'] = df['name'].apply(
                lambda name: detect_gender_bias_with_inference(name) if pd.notnull(name) else "unknown"
            )

        # Calculate quality and compliance metrics
        quality_issues = df['duplicate_flag'].sum() + df['missing_message'].sum() + df['missing_name'].sum()
        pii_entries = df[['email_flag', 'ssn_flag', 'phone_flag']].sum().sum() if pii_detection else 0

        quality_score = (total_entries - quality_issues) / total_entries
        compliance_score = (total_entries - pii_entries) / total_entries

        # Thresholds with customization options
        quality_threshold = st.slider("Set Quality Threshold", 0.0, 1.0, 0.9)
        compliance_threshold = st.slider("Set Compliance Threshold", 0.0, 1.0, 0.95)
        st.write("Threshold Levels: 0.8 or below = Low, 0.9 = Moderate, 1.0 = High")

        # High-Level Summary
        st.write("### Overall Assessment Summary")
        overall_assessment = "Data Fit for Purpose" if quality_score >= quality_threshold and compliance_score >= compliance_threshold else "Data Not Fit for Purpose"
        top_issues = []
        
        if quality_score < quality_threshold:
            top_issues.append("Quality (incomplete data, duplicates)")
        if compliance_score < compliance_threshold:
            top_issues.append("Compliance (PII detected)")
        if bias_detection and (df['language_bias_flag'].sum() > 0 or df['gender_bias_flag'].value_counts().get("unknown", 0) < total_entries):
            top_issues.append("Ethics (language or gender bias detected)")

        st.write(f"**Overall Assessment:** {overall_assessment}")
        st.write(f"**Top Issues:** {', '.join(top_issues) if top_issues else 'None'}")

        # Assessment and Conclusions with Recommendations
        if quality_score < quality_threshold:
            st.markdown("<span style='color:red;'>Data Not Fit for Purpose: Significant quality issues detected.</span>", unsafe_allow_html=True)
            st.info("Next Steps: Consider reviewing duplicate or missing entries, and ensuring data consistency across all columns.")
        else:
            st.markdown("<span style='color:green;'>Data Fit for Purpose: Quality metrics are within acceptable limits.</span>", unsafe_allow_html=True)

        if compliance_score < compliance_threshold:
            st.warning("Compliance Risk: Data may not meet regulatory standards (e.g., GDPR).")
            st.info("Next Steps: Ensure personal data is anonymized or removed where unnecessary, and review all PII-related flags.")

        # Additional Ethical Warnings with Recommendations
        if bias_detection:
            if df['language_bias_flag'].sum() > 0:
                st.warning("Potential Ethical Concerns: Language bias detected.")
                st.info("Next Steps: Review flagged entries for biased language, and rephrase terms that imply stereotypes.")
            if df['gender_bias_flag'].value_counts().get("unknown", 0) < total_entries:
                st.warning("Gender Representation Imbalance Detected.")
                st.info("Next Steps: Consider balancing gender representation in your dataset for inclusivity.")

        # Summary Visualizations
        st.write("### Quality and Compliance Metrics")
        st.write(f"Quality Score: {quality_score:.2f} | Compliance Score: {compliance_score:.2f}")

        # Bar chart for quality and PII issues
        fig, ax = plt.subplots()
        ax.bar(["Quality Issues", "PII Issues"], [quality_issues, pii_entries])
        ax.set_ylabel("Number of Issues")
        st.pyplot(fig)

        # Pie charts for quality and compliance
        for title, data, labels in [
            ("Data Quality Distribution", [quality_score, 1 - quality_score], ["Quality", "Issues"]),
            ("Compliance Distribution", [compliance_score, 1 - compliance_score], ["Compliant", "Non-compliant"]),
        ]:
            fig, ax = plt.subplots()
            ax.pie(data, labels=labels, autopct="%1.1f%%", startangle=90)
            ax.set_title(title)
            st.pyplot(fig)

        # Contextual Resources
        with st.expander("What is Language Bias?"):
            st.write("Language bias refers to terms or phrases that perpetuate stereotypes. Learn more about [ethical language usage](https://example.com/ethical-language).")
        with st.expander("Why is Gender Representation Important?"):
            st.write("Balanced gender representation helps avoid perpetuating stereotypes and ensures inclusivity. Read more about [gender bias in AI](https://example.com/gender-bias).")

        # Generate report
        output_path = "report.txt"
        generate_report(df, output_path=output_path)
        
        st.write("Analysis Complete! Summary Report:")
        with open(output_path, "r") as report_file:
            st.text(report_file.read())

        # Download button for the report
        with open(output_path, "rb") as file:
            st.download_button(
                label="Download Report",
                data=file,
                file_name="Dataset_Quality_Report.txt",
                mime="text/plain"
            )
    else:
        st.warning("Please upload a CSV file.")
