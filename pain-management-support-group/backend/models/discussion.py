"""
Discussion forum models for patient interaction
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .base import Base


class DiscussionPost(Base):
    """Discussion forum post"""
    __tablename__ = "discussion_posts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    title = Column(String(300), nullable=False)
    content = Column(Text, nullable=False)

    # Categorization
    category = Column(String(100), nullable=True)  # e.g., "pain management", "nutrition", etc.
    tags = Column(Text, nullable=True)  # JSON string

    # Moderation
    is_approved = Column(Boolean, default=True)
    is_pinned = Column(Boolean, default=False)
    is_locked = Column(Boolean, default=False)

    # Engagement
    views_count = Column(Integer, default=0)
    likes_count = Column(Integer, default=0)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="discussion_posts")
    replies = relationship("DiscussionReply", back_populates="post", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<DiscussionPost(id={self.id}, title='{self.title}', user={self.user_id})>"

    @property
    def reply_count(self):
        """Count of replies"""
        return len(self.replies) if self.replies else 0


class DiscussionReply(Base):
    """Reply to a discussion post"""
    __tablename__ = "discussion_replies"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("discussion_posts.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    parent_reply_id = Column(Integer, ForeignKey("discussion_replies.id"), nullable=True)  # For nested replies

    content = Column(Text, nullable=False)

    # Moderation
    is_approved = Column(Boolean, default=True)

    # Engagement
    likes_count = Column(Integer, default=0)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    post = relationship("DiscussionPost", back_populates="replies")
    user = relationship("User")
    parent_reply = relationship("DiscussionReply", remote_side=[id], backref="child_replies")

    def __repr__(self):
        return f"<DiscussionReply(id={self.id}, post={self.post_id}, user={self.user_id})>"
