import os
import random
import google.generativeai as genai
from dotenv import load_dotenv
from typing import List  # Add this import

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-pro")

def generate_prompt(conversation: list[str]) -> str:
    chat_text = " ".join(conversation)
    response = model.generate_content(
        f"Convert this conversation into a detailed, richly textured, hyperpersonalized painting prompt: {chat_text}. "
        "Ensure it captures all key details, emotions, and nuances, with vivid imagery and artistic flair."
    )
    return response.text

def generate_images(prompt: str) -> List[str]:  # Now List is defined
    return [
        f"image_{random.randint(1, 1000)}",
        f"image_{random.randint(1, 1000)}",
        f"image_{random.randint(1, 1000)}"
    ]