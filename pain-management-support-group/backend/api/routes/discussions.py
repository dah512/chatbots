"""Discussion forum routes"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.models.base import get_db
from backend.models.user import User
from backend.api.routes.auth import get_current_active_user

router = APIRouter()

@router.get("/posts")
async def get_posts(db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    """Get discussion posts"""
    return {"message": "Discussion posts"}

@router.post("/posts")
async def create_post(db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    """Create discussion post"""
    return {"message": "Create post"}
