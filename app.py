import streamlit as st
from utils import preprocess_image, extract_text, structure_data, generate_explanations
from PIL import Image

st.set_page_config(page_title="AI Medical Report Analyzer", layout="wide")
st.title("🩺 AI-Powered Medical Report Analyzer")
st.markdown("Upload a scanned medical report image (PNG, JPG) and get explanations for test results.")

uploaded_file = st.file_uploader("Upload an image file", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Report", use_column_width=True)

    st.info("Preprocessing and extracting data...")
    processed = preprocess_image(image)
    text = extract_text(processed)

    st.subheader("Extracted Text")
    st.text(text)

    data = structure_data(text)
    if not data.empty:
        st.subheader("Structured Test Data")
        st.dataframe(data)

        st.subheader("AI Explanations")
        explanations = generate_explanations(data)
        for item in explanations:
            with st.expander(f"{item['Test Name']} ({item['Status']})"):
                st.write(item['Explanation'])
    else:
        st.warning("No valid test data found in the report.")