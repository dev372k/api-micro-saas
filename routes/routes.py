from fastapi import APIRouter
from models.requests.optimize_request import OptimizeRequest
from utils.optimizer import optimized_text

router = APIRouter()

@router.post("/optimize")
def optimize_text(req: OptimizeRequest):
    return optimized_text(req.text, mode=req.mode, model=req.model)