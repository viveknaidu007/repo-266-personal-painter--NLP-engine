from fastapi import FastAPI
from app.routes import chat, search

app = FastAPI(title="Personal Painter API")

app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
app.include_router(search.router, prefix="/api/search", tags=["search"])

@app.get("/")
async def root():
    return {"message": "Welcome to Personal Painter API"}