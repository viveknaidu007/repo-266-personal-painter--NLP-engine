from fastapi import APIRouter
from app.models.schemas import ChatMessage, ChatResponse
from app.services.painter import generate_prompt, generate_images

router = APIRouter()
conversation = []

@router.post("/chat", response_model=ChatResponse)
async def chat_with_painter(message: ChatMessage):
    conversation.append(message.message)
    prompt = generate_prompt(conversation)
    images = generate_images(prompt)
    return ChatResponse(prompt=prompt, images=images)

@router.get("/reset-chat")
async def reset_chat():
    conversation.clear()
    return {"message": "Conversation reset"}