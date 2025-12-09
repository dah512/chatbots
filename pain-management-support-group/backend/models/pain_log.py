"""
Pain logging and tracking models
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from .base import Base


class PainLocation(str, enum.Enum):
    """Common pain locations"""
    LOWER_BACK = "lower_back"
    UPPER_BACK = "upper_back"
    NECK = "neck"
    SHOULDER_LEFT = "shoulder_left"
    SHOULDER_RIGHT = "shoulder_right"
    HIP_LEFT = "hip_left"
    HIP_RIGHT = "hip_right"
    KNEE_LEFT = "knee_left"
    KNEE_RIGHT = "knee_right"
    ANKLE_LEFT = "ankle_left"
    ANKLE_RIGHT = "ankle_right"
    HAND_LEFT = "hand_left"
    HAND_RIGHT = "hand_right"
    FOOT_LEFT = "foot_left"
    FOOT_RIGHT = "foot_right"
    HEAD = "head"
    CHEST = "chest"
    ABDOMEN = "abdomen"
    WHOLE_BODY = "whole_body"
    OTHER = "other"


class PainLog(Base):
    """Daily pain log entry"""
    __tablename__ = "pain_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Pain assessment
    pain_level = Column(Integer, nullable=False)  # VAS 0-10
    pain_locations = Column(Text, nullable=False)  # JSON string of locations
    pain_quality = Column(Text, nullable=True)  # e.g., "sharp", "dull", "burning"

    # Activity and triggers
    activity_before_pain = Column(Text, nullable=True)
    pain_triggers = Column(Text, nullable=True)

    # Management strategies used
    medications_taken = Column(Text, nullable=True)  # JSON string
    non_med_strategies = Column(Text, nullable=True)  # What worked/didn't work

    # Impact on function
    sleep_quality = Column(Integer, nullable=True)  # 0-10 scale
    fatigue_level = Column(Integer, nullable=True)  # 0-10 scale
    anxiety_level = Column(Integer, nullable=True)  # 0-10 scale
    function_level = Column(Integer, nullable=True)  # 0-10 scale

    # ADL completion
    adls_completed = Column(Text, nullable=True)  # JSON string
    adls_difficulty = Column(Text, nullable=True)  # JSON string

    # Notes
    notes = Column(Text, nullable=True)

    # Weather (can affect pain)
    weather_conditions = Column(String(100), nullable=True)

    # Log date (separate from created_at for backdating)
    log_date = Column(DateTime(timezone=True), nullable=False, index=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="pain_logs")

    def __repr__(self):
        return f"<PainLog(id={self.id}, user={self.user_id}, pain={self.pain_level}, date={self.log_date})>"
