"""
User model for authentication and profile management
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum as SQLEnum, Text, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
import enum

from .base import Base


class UserRole(str, enum.Enum):
    """User role enumeration"""
    PATIENT = "patient"
    INSTRUCTOR = "instructor"
    ADMIN = "admin"
    FACILITATOR = "facilitator"


class User(Base):
    """User model for authentication and profile"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)

    # Profile Information
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    date_of_birth = Column(Date, nullable=True)
    phone = Column(String(20), nullable=True)

    # Role and Status
    role = Column(SQLEnum(UserRole), default=UserRole.PATIENT, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)

    # Medical Information (for patients)
    primary_pain_condition = Column(String(200), nullable=True)
    pain_conditions = Column(Text, nullable=True)  # JSON string of conditions list
    current_medications = Column(Text, nullable=True)  # JSON string
    allergies = Column(Text, nullable=True)
    other_health_conditions = Column(Text, nullable=True)

    # Program Enrollment
    enrollment_date = Column(DateTime(timezone=True), nullable=True)
    program_start_date = Column(DateTime(timezone=True), nullable=True)
    program_completion_date = Column(DateTime(timezone=True), nullable=True)
    current_week = Column(Integer, default=1)

    # Preferences
    preferred_session_times = Column(Text, nullable=True)  # JSON string
    dietary_restrictions = Column(Text, nullable=True)
    mobility_limitations = Column(Text, nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    last_login = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    pain_logs = relationship("PainLog", back_populates="user", cascade="all, delete-orphan")
    assessment_submissions = relationship("AssessmentSubmission", back_populates="user", cascade="all, delete-orphan")
    progress_tracking = relationship("ProgressTracking", back_populates="user", cascade="all, delete-orphan")
    discussion_posts = relationship("DiscussionPost", back_populates="user", cascade="all, delete-orphan")
    rag_conversations = relationship("RAGConversation", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', role='{self.role}')>"

    @property
    def full_name(self):
        """Return full name"""
        return f"{self.first_name} {self.last_name}"

    @property
    def is_patient(self):
        """Check if user is a patient"""
        return self.role == UserRole.PATIENT

    @property
    def is_instructor(self):
        """Check if user is an instructor"""
        return self.role == UserRole.INSTRUCTOR

    @property
    def is_admin(self):
        """Check if user is an admin"""
        return self.role == UserRole.ADMIN
