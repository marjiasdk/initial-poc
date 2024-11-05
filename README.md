# Evadence: Ensuring Quality, Compliance, and Ethical Standards for AI Training Data

Evadence is a tool designed to help organizations validate that their datasets meet essential quality, compliance, and ethical standards for AI training. Focusing on purpose-fit data, Evadence analyzes whether a dataset is relevant, compliant, and unbiased, ensuring it’s suitable for the AI model’s intended purpose.

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

## Usage

1. **Install Dependencies:** Run ``pip install -r requirements.txt`` to install the required packages.
2. **Set Up the API Key**: Place your Cerebras API key in a ``.env`` file in the following format: ``CEREBRAS_API_KEY=your_api_key_here``
3. **Run the Application**: Start the Streamlit app by running: ``streamlit run app.py``
4. **Access the Tool**: Once running, you can access the tool in your web browser at ``http://localhost:8501``.

---

## Example Workflow

1. **Data Upload**: Upload your dataset in CSV format for analysis.
2. **Select Analysis Options**: Choose between relevance, PII, and bias checks, or run all for a comprehensive analysis.
3. **Review Results**: Examine the interactive metrics and compliance results within the app.
4. **Download Report**: Export a summary report of the analysis results.

---

## Notes on Deployment

This tool is designed for local testing and development, leveraging the Cerebras Cloud API for enhanced inference speeds. If you wish to deploy it to a cloud service (such as Streamlit Cloud), please ensure that sensitive information, particularly the API key, remains secure. Using environment variables and never hardcoding the API key directly into any public repositories is strongly recommended.

---

## Demo

[Watch the Demo Video on Google Drive](https://drive.google.com/file/d/10CIBxk2GZ83oPvtkOco0QmSTAI-Z9hyT/view?usp=sharing)

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
