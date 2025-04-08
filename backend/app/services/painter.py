import os
from typing import List
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

def generate_prompt(conversation: list[str]) -> str:
    chat_text = " ".join(conversation)
    try:
        response = model.generate_content(
            f"Convert this conversation into a detailed, richly textured, hyperpersonalized painting prompt: {chat_text}. "
            "Ensure it captures all key details, emotions, and nuances, with vivid imagery and artistic flair. Return only the prompt text."
        )
        print(f"Gemini Response: {response.text}")  # Debug
        return response.text
    except Exception as e:
        print(f"Gemini Error: {e}")  # Debug
        return f"Error: Unable to generate prompt due to {str(e)}"

def generate_images(prompt: str) -> List[str]:
    return []