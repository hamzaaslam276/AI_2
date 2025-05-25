import cv2
import numpy as np
import pytesseract
import re
import pandas as pd
from openai import OpenAI
import streamlit as st
import pytesseract

pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def preprocess_image(pil_image):
    image = np.array(pil_image)
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return binary

def extract_text(image):
    return pytesseract.image_to_string(image)

def structure_data(text):
    pattern = r"([A-Za-z ]+):?\s*(\d+(\.\d+)?)\s*(mg/dL|g/dL|%)?\s*[-–]?\s*(\d+(\.\d+)?)[-–](\d+(\.\d+)?)"
    matches = re.findall(pattern, text)
    records = []
    for match in matches:
        test_name = match[0].strip()
        value = float(match[1])
        unit = match[3]
        normal_low = float(match[4])
        normal_high = float(match[6])
        status = "Normal"
        if value < normal_low:
            status = "Low"
        elif value > normal_high:
            status = "High"
        records.append({
            "Test Name": test_name,
            "Value": value,
            "Unit": unit,
            "Normal Range": f"{normal_low}-{normal_high}",
            "Status": status
        })
    return pd.DataFrame(records)

def generate_explanations(df):
    explanations = []
    for _, row in df.iterrows():
        if row["Status"] == "Normal":
            continue
        prompt = (
            f"Explain in simple terms what it means if the patient's {row['Test Name']} is {row['Value']} {row['Unit']} "
            f"and the normal range is {row['Normal Range']}."
        )
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=150
            )
            explanation = response.choices[0].message.content.strip()
        except Exception as e:
            explanation = f"Error: {e}"
        explanations.append({
            "Test Name": row["Test Name"],
            "Status": row["Status"],
            "Explanation": explanation
        })
    return explanations