"""
Resource models for educational materials and visual aids
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Enum as SQLEnum
from sqlalchemy.sql import func
import enum

from .base import Base


class ResourceType(str, enum.Enum):
    """Type of resource"""
    VISUAL_AID = "visual_aid"
    SLIDE = "slide"
    HANDOUT = "handout"
    VIDEO = "video"
    DOCUMENT = "document"
    INFOGRAPHIC = "infographic"
    ANATOMY_DIAGRAM = "anatomy_diagram"
    EXERCISE_GUIDE = "exercise_guide"
    NUTRITION_GUIDE = "nutrition_guide"
    RESEARCH_PAPER = "research_paper"


class Resource(Base):
    """Educational resource or material"""
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(300), nullable=False)
    description = Column(Text, nullable=True)
    resource_type = Column(SQLEnum(ResourceType), nullable=False, index=True)

    # File information
    file_url = Column(String(500), nullable=False)
    file_size_bytes = Column(Integer, nullable=True)
    file_format = Column(String(20), nullable=True)  # pdf, jpg, mp4, etc.
    thumbnail_url = Column(String(500), nullable=True)

    # Categorization
    category = Column(String(100), nullable=True)
    tags = Column(Text, nullable=True)  # JSON string
    week_number = Column(Integer, nullable=True, index=True)
    session_number = Column(Integer, nullable=True, index=True)

    # Content metadata
    author = Column(String(200), nullable=True)
    source = Column(String(300), nullable=True)
    publication_date = Column(DateTime(timezone=True), nullable=True)

    # Access control
    is_published = Column(Boolean, default=True)
    is_featured = Column(Boolean, default=False)
    requires_enrollment = Column(Boolean, default=False)

    # Engagement tracking
    views_count = Column(Integer, default=0)
    downloads_count = Column(Integer, default=0)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<Resource(id={self.id}, title='{self.title}', type='{self.resource_type}')>"
