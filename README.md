# Dataset Quality and Compliance Tool

This tool is a **Streamlit-based web application** designed for assessing dataset quality, compliance, and bias detection. It leverages the **Cerebras Cloud API** for high-speed inference, making it an efficient solution for analyzing dataset suitability for AI model training, as well as identifying potential compliance and ethical concerns.

---

## Overview

### Features
- **Quality Assessment**: Checks for data relevance, completeness, duplicates, and language quality.
- **Compliance Check**: Flags Personally Identifiable Information (PII) such as emails, Social Security numbers (SSNs), and phone numbers.
- **Bias Detection**: Detects potential biases in language and gender representation within the dataset.

### Built With
- **Cerebras Cloud SDK**: Utilizes the Cerebras API for fast inference during compliance and bias checks.
- **Streamlit**: Provides an interactive web application interface.
- **Python & Pandas**: For data processing and analysis.

---

## Example Workflow

1. **Data Upload**: Upload your dataset in CSV format for analysis.
2. **Select Analysis Options**: Choose between relevance, PII, and bias checks, or run all for a comprehensive analysis.
3. **Review Results**: Examine the interactive metrics and compliance results within the app.
4. **Download Report**: Export a summary report of the analysis results.

---

## Demo

[Watch the Demo Video on Google Drive](https://drive.google.com/yourvideolink)

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
