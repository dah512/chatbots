"""
Curriculum routes for weeks and sessions
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel

from backend.models.base import get_db
from backend.models.curriculum import Week, Session as SessionModel
from backend.models.user import User
from backend.api.routes.auth import get_current_active_user

router = APIRouter()


class WeekResponse(BaseModel):
    id: int
    week_number: int
    title: str
    theme: str
    description: str

    class Config:
        from_attributes = True


class SessionResponse(BaseModel):
    id: int
    session_number: int
    overall_session_number: int
    title: str
    description: str
    duration_minutes: int

    class Config:
        from_attributes = True


@router.get("/weeks", response_model=List[WeekResponse])
async def get_all_weeks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get all curriculum weeks"""
    weeks = db.query(Week).order_by(Week.week_number).all()
    return weeks


@router.get("/week/{week_number}", response_model=WeekResponse)
async def get_week(
    week_number: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get specific week details"""
    week = db.query(Week).filter(Week.week_number == week_number).first()
    if not week:
        raise HTTPException(status_code=404, detail="Week not found")
    return week


@router.get("/week/{week_number}/sessions", response_model=List[SessionResponse])
async def get_week_sessions(
    week_number: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get sessions for a specific week"""
    week = db.query(Week).filter(Week.week_number == week_number).first()
    if not week:
        raise HTTPException(status_code=404, detail="Week not found")

    sessions = db.query(SessionModel).filter(
        SessionModel.week_id == week.id
    ).order_by(SessionModel.session_number).all()
    return sessions


@router.get("/session/{session_id}", response_model=SessionResponse)
async def get_session(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get specific session details"""
    session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session
