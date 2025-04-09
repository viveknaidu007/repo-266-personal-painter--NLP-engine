from fastapi import APIRouter, HTTPException
from app.models.schemas import ChatMessage, ChatResponse
from app.services.painter import generate_prompt, generate_images

router = APIRouter()
conversation = []

@router.post("", response_model=ChatResponse)
async def chat_with_painter(message: ChatMessage):
    try:
        # Append new message to conversation
        conversation.append(message.message)
        full_conversation = message.conversation + [message.message] if message.conversation else [message.message]
        
        # Generate prompt based on full conversation
        prompt = generate_prompt(full_conversation)
        images = generate_images(prompt)  # Generate 3 images
        print(f"Debug: Prompt = {prompt}, Images = {images}")
        return ChatResponse(prompt=prompt, images=images)
    except Exception as e:
        print(f"Error in chat_with_painter: {e}")
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

@router.get("/reset-chat")
async def reset_chat():
    conversation.clear()
    return {"message": "Conversation reset"}