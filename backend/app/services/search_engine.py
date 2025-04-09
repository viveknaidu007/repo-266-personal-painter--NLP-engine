import json
from typing import List, Dict

with open("app/data/images.json", "r") as f:
    IMAGE_DATA = json.load(f)

def calculate_convergence(query: str, description: str, labels: List[str]) -> float:
    # Simple convergence: count overlapping words in query, description, and labels
    query_words = set(query.lower().split())
    desc_words = set(description.lower().split())
    label_words = set(labels)
    overlap = len(query_words.intersection(desc_words.union(label_words)))
    total_query_words = len(query_words)
    return overlap / total_query_words if total_query_words > 0 else 0

def search_images(query: str) -> List[Dict]:
    results = []
    for image in IMAGE_DATA:
        score = calculate_convergence(query, image["description"], image["labels"])
        results.append({**image, "score": score})
    return sorted(results, key=lambda x: x["score"], reverse=True)

def search_collections(query: str) -> List[Dict]:
    image_results = search_images(query)
    collection = {
        "collection_id": 1,
        "images": image_results[:5],
        "avg_score": sum(img["score"] for img in image_results[:5]) / 5 if image_results else 0
    }
    return [collection]