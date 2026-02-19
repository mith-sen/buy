from PIL import Image
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

def extract_text_from_image(image_file):
    image = Image.open(image_file)
    response = model.generate_content([
        "Extract all text from this product label or bill image. Return only the raw text found.",
        image
    ])
    return response.text