# 🩺 AI-Powered Medical Report Analyzer (OpenAI v1.x)

This project extracts and explains medical lab test results using OCR + OpenAI GPT-3.5.

## Features
- Upload a scanned medical report image
- Extract test names, values, units, and normal ranges
- AI explains abnormal test results in simple language

## Deployment on Streamlit Cloud
1. Push this repo to GitHub
2. Go to [streamlit.io/cloud](https://streamlit.io/cloud) and deploy the app
3. Add your OpenAI key to **Secrets**:
```
OPENAI_API_KEY = "your-key-here"
```

## Local Usage
```bash
pip install -r requirements.txt
streamlit run app.py
```