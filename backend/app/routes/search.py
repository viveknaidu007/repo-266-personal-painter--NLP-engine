from fastapi import APIRouter, HTTPException
from app.models.schemas import SearchRequest, SearchResponse, ImageResult, CollectionResult
from app.services.search_engine import search_images, search_collections

router = APIRouter()

@router.post("", response_model=SearchResponse)
async def search(request: SearchRequest):
    try:
        if request.search_type not in ["image", "collection"]:
            raise HTTPException(status_code=400, detail="Invalid search_type")
        if request.search_type == "image":
            results = search_images(request.query)
            formatted_results = [ImageResult(**r) for r in results[:20]]  # Top 20
        else:
            results = search_collections(request.query)
            formatted_results = [CollectionResult(**r) for r in results[:5]]  # Top 5
        return SearchResponse(results=formatted_results)
    except Exception as e:
        print(f"Error in search: {e}")
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")