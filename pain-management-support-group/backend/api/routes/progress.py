"""Progress tracking routes"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.models.base import get_db
from backend.models.user import User
from backend.api.routes.auth import get_current_active_user

router = APIRouter()

@router.get("/overview")
async def get_progress_overview(db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    """Get overall progress"""
    return {"message": "Progress overview"}

@router.get("/week/{week_num}")
async def get_week_progress(week_num: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    """Get week-specific progress"""
    return {"message": f"Week {week_num} progress"}
