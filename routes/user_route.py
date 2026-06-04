from fastapi import APIRouter

user_router = APIRouter(prefix="/users", tags=["users"])

@user_router.post("/")
def optimize_text():
    return {
        "original_text": "Sample text",
        "optimized_text": "Optimized (default): Sample text...",
    }