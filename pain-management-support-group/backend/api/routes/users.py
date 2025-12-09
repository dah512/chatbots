"""
User profile and management routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

from backend.models.base import get_db
from backend.models.user import User, UserRole
from backend.api.routes.auth import get_current_active_user

router = APIRouter()


class UserProfileUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    primary_pain_condition: Optional[str] = None
    dietary_restrictions: Optional[str] = None
    mobility_limitations: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    first_name: str
    last_name: str
    role: UserRole
    current_week: int
    primary_pain_condition: Optional[str]

    class Config:
        from_attributes = True


@router.get("/profile", response_model=UserResponse)
async def get_profile(
    current_user: User = Depends(get_current_active_user)
):
    """Get current user's profile"""
    return current_user


@router.put("/profile", response_model=UserResponse)
async def update_profile(
    profile_update: UserProfileUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update user profile"""
    for field, value in profile_update.dict(exclude_unset=True).items():
        setattr(current_user, field, value)

    db.commit()
    db.refresh(current_user)
    return current_user


@router.get("/dashboard")
async def get_dashboard(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get user dashboard data"""
    return {
        "user": {
            "name": current_user.full_name,
            "current_week": current_user.current_week,
            "enrollment_date": current_user.enrollment_date
        },
        "stats": {
            "sessions_attended": 0,  # TODO: Calculate from progress tracking
            "assessments_completed": 0,  # TODO: Calculate
            "pain_logs": 0,  # TODO: Calculate
        }
    }
