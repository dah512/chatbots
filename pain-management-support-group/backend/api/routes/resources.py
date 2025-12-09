"""Educational resources routes"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.models.base import get_db
from backend.models.user import User
from backend.models.resource import Resource, ResourceType
from backend.api.routes.auth import get_current_active_user

router = APIRouter()

@router.get("/visual-aids")
async def get_visual_aids(db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    """Get visual aids"""
    resources = db.query(Resource).filter(Resource.resource_type == ResourceType.VISUAL_AID).all()
    return resources

@router.get("/slides/{week_num}")
async def get_slides(week_num: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    """Get slides for week"""
    return {"message": f"Week {week_num} slides"}

@router.get("/materials")
async def get_materials(db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    """Get supplementary materials"""
    return {"message": "Materials"}
