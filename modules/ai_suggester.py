import os
import time
import random
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def call_groq(prompt, retries=4, base_wait_s=4):
    """Call Groq with retry/backoff on rate limit/transient errors."""
    last_err = None
    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",  # Free & fast. Alt: "mixtral-8x7b-32768"
                messages=[{"role": "user", "content": prompt}],
                max_tokens=2048,
                temperature=0.7,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            last_err = e
            err = str(e)
            retriable = (
                "429" in err
                or "rate_limit" in err.lower()
                or "quota" in err.lower()
                or "timeout" in err.lower()
                or "temporarily unavailable" in err.lower()
                or "internal" in err.lower()
            )
            if retriable and attempt < retries - 1:
                wait = base_wait_s * (2**attempt) + random.uniform(0, 0.75)
                print(f"Groq busy/rate-limited. Waiting {wait:.1f}s (retry {attempt+1}/{retries})...")
                time.sleep(wait)
            else:
                break

    return f"⚠️ Could not get a response from AI. Please try again in a minute.\n\nError: `{last_err}`"


def get_ai_analysis(extracted_text):
    """
    Single-call analysis (faster + less rate limiting).
    Returns dict with markdown strings for tabs: health / eco / alternatives.
    """
    prompt = f"""
You are an expert assistant for consumers. Analyze the text below (bill/product label/ingredients).

TEXT:
{extracted_text}

Rules:
- Output ONLY clean markdown. No greetings, no intro.
- Use short bullets. Use **bold** for ingredient/item names when relevant.
- Keep each section self-contained.

Return EXACTLY these three sections in order, with these headings:

## 🥗 Health & Risks
Include:
- 6-12 bullets of health analysis
- 3-6 bullets of health risks

## 🌍 Eco Impact
Include:
- Packaging impact (2-4 bullets)
- Carbon footprint (2-4 bullets)
- Sustainability rating: **Poor / Fair / Good / Excellent** with one-sentence reason
- How to make it more eco-friendly (4-6 bullets)

## 💡 Alternatives & Recipe
Include:
- Exactly 3 healthier store-bought alternatives in the format:
  **1. [Product Name]** – [Why it's healthier]
- A simple homemade recipe with:
  **Ingredients:** (bullets)
  **Steps:** (numbered)
"""

    full = call_groq(prompt)
    if not full or not isinstance(full, str):
        return "⚠️ Empty AI response. Please try again."

    # Split into the three tab contents
    try:
        h = full.split("## 🥗 Health & Risks", 1)[1]
        parts_after_health = h.split("## 🌍 Eco Impact", 1)
        health_md = "## 🥗 Health & Risks" + parts_after_health[0]

        eco_and_rest = parts_after_health[1].split("## 💡 Alternatives & Recipe", 1)
        eco_md = "## 🌍 Eco Impact" + eco_and_rest[0]
        alt_md = "## 💡 Alternatives & Recipe" + eco_and_rest[1]

        return {"health": health_md.strip(), "eco": eco_md.strip(), "alternatives": alt_md.strip()}
    except Exception:
        return {"health": full, "eco": full, "alternatives": full}