"""Pain tracking routes"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from datetime import datetime

from backend.models.base import get_db
from backend.models.user import User
from backend.models.pain_log import PainLog
from backend.api.routes.auth import get_current_active_user

router = APIRouter()


class PainLogCreate(BaseModel):
    pain_level: int
    pain_locations: str
    pain_quality: str = None
    medications_taken: str = None
    notes: str = None


@router.post("/log")
async def create_pain_log(
    pain_log: PainLogCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Log pain entry"""
    new_log = PainLog(
        user_id=current_user.id,
        log_date=datetime.utcnow(),
        **pain_log.dict()
    )
    db.add(new_log)
    db.commit()
    return {"message": "Pain log created", "id": new_log.id}


@router.get("/history")
async def get_pain_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    limit: int = 30
):
    """Get pain history"""
    logs = db.query(PainLog).filter(
        PainLog.user_id == current_user.id
    ).order_by(PainLog.log_date.desc()).limit(limit).all()
    return logs


@router.get("/analytics")
async def get_pain_analytics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get pain analytics"""
    return {"message": "Pain analytics endpoint"}
