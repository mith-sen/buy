import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.0-flash-lite")

def extract_text_from_image(image_file):
    image = Image.open(image_file)
    
    # Convert to RGB if needed
    if image.mode != "RGB":
        image = image.convert("RGB")
    
    # Resize if too large (reduces API usage)
    max_size = (800, 800)
    image.thumbnail(max_size, Image.LANCZOS)
    
    # Convert to bytes
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='JPEG', quality=85)
    img_byte_arr.seek(0)
    
    image_data = {
        "mime_type": "image/jpeg",
        "data": img_byte_arr.getvalue()
    }
    
    response = model.generate_content([
        "Extract all visible text from this product label or receipt image. Return only the raw text.",
        image_data
    ])
    return response.text