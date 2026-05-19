from fastapi import APIRouter
from models.schemas import OptimizeRequest

router = APIRouter()

@router.post("/optimize")
def optimize_text(req: OptimizeRequest):
    return {
        "original_text": req.text,
        "optimized_text": f"Optimized ({req.mode}): {req.text[:50]}...",
    }