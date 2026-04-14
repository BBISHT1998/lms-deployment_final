from fastapi import APIRouter
from app.utils.chroma_db import search_chroma

router = APIRouter()

@router.get("/search")
def search_notes(q: str):
    results = search_chroma(q)

    return {
        "query": q,
        "documents": results.get("documents", []),
        "ids": results.get("ids", [])
    }