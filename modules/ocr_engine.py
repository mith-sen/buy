from PIL import Image
import os
import io
import base64
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def extract_text_from_image(image_file):
    image = Image.open(image_file)
    image = image.convert("RGB")

    # Downscale big uploads to speed up OCR + reduce quota usage.
    max_dim = 1280
    if max(image.size) > max_dim:
        image.thumbnail((max_dim, max_dim), Image.Resampling.LANCZOS)

    # Encode image to base64 JPEG for Groq vision API
    buf = io.BytesIO()
    image.save(buf, format="JPEG", quality=80, optimize=True)
    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode("utf-8")

    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",  # Groq's free vision model
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_base64}",
                        },
                    },
                    {
                        "type": "text",
                        "text": "Extract all visible text from this receipt/product label image. Return only the raw text, nothing else.",
                    },
                ],
            }
        ],
        max_tokens=1024,
    )

    return response.choices[0].message.content.strip()