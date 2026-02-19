import streamlit as st
from groq import Groq

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

def get_ai_analysis(extracted_text):
    prompt = f"""
    You are a smart health and eco assistant. Analyze this product label or bill text:

    {extracted_text}

    Provide the following:
    1. HEALTH ANALYSIS - Identify harmful ingredients (sugar, sodium, preservatives, allergens)
    2. HEALTH RISKS - What risks does this product pose?
    3. ECO IMPACT - Comment on packaging and environmental impact
    4. HEALTHIER ALTERNATIVES - Suggest 3 better store-bought alternatives
    5. HOMEMADE RECIPE - Give a simple homemade version of this product

    Be concise and practical.
    """
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1024
    )
    return response.choices[0].message.content

