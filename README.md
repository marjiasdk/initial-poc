# Dataset Quality and Compliance Tool

This tool is a **Streamlit-based web application** that provides a comprehensive analysis of dataset quality, compliance, and bias detection, leveraging the **Cerebras Cloud API** for fast inference. The tool is designed to help users assess dataset suitability for training AI models and to flag any potential compliance and ethical issues.

## Overview

### Features
- **Quality Assessment**: Checks for data relevance, completeness, duplicates, and language quality.
- **Compliance Check**: Flags personally identifiable information (PII) such as email addresses, SSNs, and phone numbers.
- **Bias Detection**: Identifies potential biases in language and gender representation within the dataset.

### Built With
- **Cerebras Cloud SDK**: Utilizes the Cerebras API for fast inference during compliance and bias checks.
- **Streamlit**: Provides an interactive web application interface.
- **Python and Pandas**: For data processing and analysis.

## Example Workflow
- Data Upload: Upload a CSV dataset for analysis.
- Select Analysis Options: Choose relevance, PII, or bias checks, or run all for a full analysis.
- Review Results: Examine the interactive metrics and compliance results.
- Download Report: Export the summary report as a CSV.

## Demo
[Demo Video on Google Drive]([https://drive.google.com/file/d/10CIBxk2GZ83oPvtkOco0QmSTAI-Z9hyT/view?usp=sharing])

## License
This project is licensed under the MIT License. See the LICENSE file for details.
