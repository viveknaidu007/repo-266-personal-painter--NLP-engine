from pydantic import BaseModel
from typing import List

class ChatMessage(BaseModel):
    message: str

class ChatResponse(BaseModel):
    prompt: str
    images: List[str] = []  # Default to empty list

class SearchRequest(BaseModel):
    query: str
    search_type: str  # "image" or "collection"

class ImageResult(BaseModel):
    id: int
    description: str
    labels: List[str]
    score: float

class CollectionResult(BaseModel):
    collection_id: int
    images: List[ImageResult]
    avg_score: float

class SearchResponse(BaseModel):
    results: List[ImageResult] | List[CollectionResult]