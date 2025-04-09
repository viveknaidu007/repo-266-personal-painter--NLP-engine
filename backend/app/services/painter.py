import os
from typing import List
from dotenv import load_dotenv
import google.generativeai as genai
import requests
from io import BytesIO
from PIL import Image
import base64

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

# Hugging Face Inference API endpoint
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY", "your_hf_api_key_here")
API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"

def generate_prompt(conversation: list[str]) -> str:
    chat_text = " ".join(conversation)
    try:
        response = model.generate_content(
            f"Convert this conversation into a detailed, richly textured, hyperpersonalized painting prompt: {chat_text}. "
            "Ensure it captures all key details, emotions, and nuances, with vivid imagery and artistic flair. Return only the prompt text."
        )
        print(f"Gemini Response: {response.text}")
        return response.text
    except Exception as e:
        print(f"Gemini Error: {e}")
        return f"Error: Unable to generate prompt due to {str(e)}"

def generate_images(prompt: str) -> List[str]:
    try:
        if not HUGGINGFACE_API_KEY or HUGGINGFACE_API_KEY == "your_hf_api_key_here":
            raise ValueError("HUGGINGFACE_API_KEY not configured in .env")
        headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
        payload = {
            "inputs": prompt,
            "num_images": 3,  # Request 3 images
            "wait_for_model": True  # Ensure the model processes the request
        }
        response = requests.post(API_URL, headers=headers, json=payload, timeout=60)  # Increased timeout
        print(f"Status Code: {response.status_code}")
        print(f"Raw Response Content Length: {len(response.content)} bytes")
        response.raise_for_status()

        if response.status_code == 200 and response.content:
            # Handle raw image data
            image_data = response.content
            if len(image_data) > 0:
                images = []
                # Attempt to load as a single image first
                try:
                    image = Image.open(BytesIO(image_data))
                    # Convert to base64 for frontend compatibility
                    buffered = BytesIO()
                    image.save(buffered, format="JPEG")
                    images.append(base64.b64encode(buffered.getvalue()).decode('utf-8'))
                except Exception as e:
                    print(f"Error loading single image: {e}")
                    # If single image fails, approximate split for 3 images (simplified)
                    part_size = len(image_data) // 3
                    for i in range(3):
                        start = i * part_size
                        end = start + part_size if i < 2 else len(image_data)
                        img_bytes = image_data[start:end]
                        try:
                            img = Image.open(BytesIO(img_bytes))
                            buffered = BytesIO()
                            img.save(buffered, format="JPEG")
                            images.append(base64.b64encode(buffered.getvalue()).decode('utf-8'))
                        except Exception as e:
                            print(f"Error loading image part {i+1}: {e}")
                            images.append("")  # Placeholder if failed
                return images
        else:
            print(f"Invalid response: {response.text}")
            return [""] * 3  # Return empty strings as placeholders
    except requests.exceptions.RequestException as e:
        print(f"Image Generation Error: {e}")
        return [""] * 3  # Return empty strings as placeholders
    except Exception as e:
        print(f"Unexpected Error: {e}")
        return [""] * 3  # Return empty strings as placeholders
