import streamlit as st
import os
from dotenv import load_dotenv
from PIL import Image
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Google Gemini AI
genai.configure(api_key=os.getenv("google_api_key"))

# Function to get response from Gemini AI
def get_gemini_response(input_text, image, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input_text, image[0], prompt])
    return response.text

# Function to process uploaded image
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [{"mime_type": uploaded_file.type, "data": bytes_data}]
        return image_parts
    else:
        return None

# Streamlit UI Configuration
st.set_page_config(page_title="Q&A Invoice Chatbot", page_icon="💬", layout="wide")

# Sidebar for branding and instructions
with st.sidebar:
    st.title("Q&A Invoice Chatbot")
    st.write("🚀 Upload an invoice image and ask questions related to it.")
    st.markdown("---")
    st.write("📌 **How it works?**")
    st.write("1. Upload an Invoice image 📸")
    st.write("2. Enter your query 📝")
    st.write("3. Click 'Submit' to get required info from Invoice⚡")

# Main UI Layout
st.title("📄 Multi-language Invoice Extractor")

# User Input Fields
input_text = st.text_input("💬 Ask a question about the invoice:", placeholder="e.g., What is the total amount?", key="input")
uploaded_file = st.file_uploader("📤 Upload Invoice Image", type=["jpg", "jpeg", "png"])

# Display uploaded image
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="🖼️ Uploaded Invoice", use_column_width=True)

# AI Prompt for Invoice Understanding
input_prompt = """
    You are an expert in understanding invoices.
    You will receive input images as invoices &
    you will have to answer questions based on the input image.
"""

# Submit button with loading animation
if st.button("🚀 Submit"):
    if uploaded_file and input_text:
        with st.spinner("Generating response... Please wait ⏳"):
            image_data = input_image_setup(uploaded_file)
            if image_data:
                response = get_gemini_response(input_prompt, image_data, input_text)
                st.success("✅ Response generated successfully!")
                st.subheader("📝 AI Response")
                st.write(response)
            else:
                st.error("❌ Error processing the image. Please try again.")
    else:
        st.warning("⚠️ Please upload an image and enter a question before submitting.")
