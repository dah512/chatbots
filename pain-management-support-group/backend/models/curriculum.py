"""
Curriculum models for weeks, sessions, and content
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .base import Base


class Week(Base):
    """Week model representing each of the 8 weeks"""
    __tablename__ = "weeks"

    id = Column(Integer, primary_key=True, index=True)
    week_number = Column(Integer, unique=True, nullable=False, index=True)
    title = Column(String(200), nullable=False)
    theme = Column(String(300), nullable=False)
    description = Column(Text, nullable=True)
    learning_objectives = Column(Text, nullable=True)  # JSON string

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    sessions = relationship("Session", back_populates="week", cascade="all, delete-orphan")
    assessments = relationship("Assessment", back_populates="week", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Week(number={self.week_number}, title='{self.title}')>"


class Session(Base):
    """Session model - 4 sessions per week, 32 total"""
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    week_id = Column(Integer, ForeignKey("weeks.id"), nullable=False)
    session_number = Column(Integer, nullable=False)  # 1-4 within the week
    overall_session_number = Column(Integer, unique=True, nullable=False, index=True)  # 1-32

    title = Column(String(300), nullable=False)
    description = Column(Text, nullable=True)
    duration_minutes = Column(Integer, default=150)  # 2.5 hours

    # Learning content
    learning_objectives = Column(Text, nullable=True)  # JSON string
    lecture_topics = Column(Text, nullable=True)  # JSON string

    # Activity content
    movement_practice = Column(Text, nullable=True)
    nutrition_topic = Column(String(200), nullable=True)

    # Materials
    slides_url = Column(String(500), nullable=True)
    handout_url = Column(String(500), nullable=True)
    video_url = Column(String(500), nullable=True)
    additional_resources = Column(Text, nullable=True)  # JSON string

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    week = relationship("Week", back_populates="sessions")
    content = relationship("SessionContent", back_populates="session", cascade="all, delete-orphan")
    progress_tracking = relationship("ProgressTracking", back_populates="session")

    def __repr__(self):
        return f"<Session(week={self.week_id}, session={self.session_number}, title='{self.title}')>"


class SessionContent(Base):
    """Detailed content blocks for each session"""
    __tablename__ = "session_content"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False)

    content_type = Column(String(50), nullable=False)  # lecture, discussion, exercise, etc.
    sequence_order = Column(Integer, nullable=False)
    title = Column(String(300), nullable=False)
    content_body = Column(Text, nullable=False)

    # Time allocation
    start_time_minutes = Column(Integer, nullable=False)  # Minutes from session start
    duration_minutes = Column(Integer, nullable=False)

    # Visual aids
    visual_aids_urls = Column(Text, nullable=True)  # JSON string of URLs
    interactive_elements = Column(Text, nullable=True)  # JSON string

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    session = relationship("Session", back_populates="content")

    def __repr__(self):
        return f"<SessionContent(session_id={self.session_id}, type='{self.content_type}')>"
