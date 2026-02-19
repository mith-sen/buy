import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash-lite")

def get_ai_analysis(extracted_text):
    prompt = f"""
    You are a smart health and eco assistant. Analyze this product label or bill text:

    {extracted_text}

    Provide the following in a clear format:
    1. 🥗 HEALTH ANALYSIS - Identify harmful ingredients (sugar, sodium, preservatives, allergens)
    2. ⚠️ HEALTH RISKS - What risks does this product pose?
    3. 🌍 ECO IMPACT - Comment on packaging and environmental impact
    4. ✅ HEALTHIER ALTERNATIVES - Suggest 3 better store-bought alternatives
    5. 🍳 HOMEMADE RECIPE - Give a simple homemade version of this product

    Be concise, friendly, and practical.
    """
    response = model.generate_content(prompt)
    return response.text