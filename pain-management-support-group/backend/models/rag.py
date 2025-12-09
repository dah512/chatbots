"""
RAG (Retrieval-Augmented Generation) models for AI Q&A conversations
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .base import Base


class RAGConversation(Base):
    """Conversation container for RAG Q&A sessions"""
    __tablename__ = "rag_conversations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    title = Column(String(300), nullable=True)  # Auto-generated or user-provided
    context = Column(Text, nullable=True)  # Optional context for the conversation

    # Conversation metadata
    is_active = Column(Boolean, default=True)
    message_count = Column(Integer, default=0)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    last_message_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    user = relationship("User", back_populates="rag_conversations")
    messages = relationship("RAGMessage", back_populates="conversation", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<RAGConversation(id={self.id}, user={self.user_id}, messages={self.message_count})>"


class RAGMessage(Base):
    """Individual message in a RAG conversation"""
    __tablename__ = "rag_messages"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("rag_conversations.id"), nullable=False)

    # Message content
    role = Column(String(20), nullable=False)  # 'user' or 'assistant'
    content = Column(Text, nullable=False)

    # RAG-specific fields
    query_embedding = Column(Text, nullable=True)  # Serialized embedding vector
    retrieved_chunks = Column(Text, nullable=True)  # JSON string of retrieved context
    sources = Column(Text, nullable=True)  # JSON string of source documents
    similarity_scores = Column(Text, nullable=True)  # JSON string of relevance scores

    # Model information
    model_used = Column(String(100), nullable=True)
    tokens_used = Column(Integer, nullable=True)
    response_time_ms = Column(Integer, nullable=True)

    # Quality feedback
    user_rating = Column(Integer, nullable=True)  # 1-5 stars
    user_feedback = Column(Text, nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    conversation = relationship("RAGConversation", back_populates="messages")

    def __repr__(self):
        return f"<RAGMessage(id={self.id}, role='{self.role}', conversation={self.conversation_id})>"
