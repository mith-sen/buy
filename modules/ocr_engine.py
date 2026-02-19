import streamlit as st
from groq import Groq
import base64
from PIL import Image
import io

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

def extract_text_from_image(image_file):
    image = Image.open(image_file)
    if image.mode != "RGB":
        image = image.convert("RGB")
    image.thumbnail((800, 800), Image.LANCZOS)
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG", quality=85)
    img_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
    response = client.chat.completions.create(
        model="llama-3.2-90b-vision-preview",
        messages=[{
            "role": "user",
            "content": [
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_base64}"}},
                {"type": "text", "text": "Extract all text from this product label or bill image. Return only the raw text found."}
            ]
        }],
        max_tokens=1024
    )
    return response.choices[0].message.content