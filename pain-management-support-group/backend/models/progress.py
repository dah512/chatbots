"""
Progress tracking models for user activities and completion
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from .base import Base


class ActivityType(str, enum.Enum):
    """Type of activity being tracked"""
    SESSION_ATTENDANCE = "session_attendance"
    ASSESSMENT_COMPLETION = "assessment_completion"
    MOVEMENT_PRACTICE = "movement_practice"
    PAIN_LOG_ENTRY = "pain_log_entry"
    DISCUSSION_POST = "discussion_post"
    RESOURCE_VIEW = "resource_view"
    HOMEWORK_COMPLETION = "homework_completion"


class ProgressTracking(Base):
    """Track user progress through program"""
    __tablename__ = "progress_tracking"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=True)

    activity_type = Column(SQLEnum(ActivityType), nullable=False)
    activity_name = Column(String(300), nullable=False)
    is_completed = Column(Boolean, default=False, nullable=False)

    # Completion details
    completion_date = Column(DateTime(timezone=True), nullable=True)
    completion_notes = Column(Text, nullable=True)

    # Scoring (if applicable)
    score = Column(Integer, nullable=True)
    max_score = Column(Integer, nullable=True)

    # Time tracking
    duration_minutes = Column(Integer, nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="progress_tracking")
    session = relationship("Session", back_populates="progress_tracking")

    def __repr__(self):
        return f"<ProgressTracking(id={self.id}, user={self.user_id}, activity='{self.activity_type}', completed={self.is_completed})>"


    @property
    def completion_percentage(self):
        """Calculate completion percentage if score exists"""
        if self.score is not None and self.max_score is not None and self.max_score > 0:
            return (self.score / self.max_score) * 100
        return None
