from fastapi import APIRouter, HTTPException
from app.models.schemas import ChatMessage, ChatResponse
from app.services.painter import generate_prompt, generate_images

router = APIRouter()
conversation = []

@router.post("", response_model=ChatResponse)  # Explicit empty path to match prefix
async def chat_with_painter(message: ChatMessage):
    try:
        conversation.append(message.message)
        prompt = generate_prompt(conversation)
        images = generate_images(prompt)
        print(f"Debug: Prompt = {prompt}, Images = {images}")  # Debug output
        return ChatResponse(prompt=prompt, images=images)
    except Exception as e:
        print(f"Error in chat_with_painter: {e}")  # Log the exception
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

@router.get("/reset-chat")
async def reset_chat():
    conversation.clear()
    return {"message": "Conversation reset"}