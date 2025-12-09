"""
RAG (Retrieval-Augmented Generation) routes for AI-powered Q&A
"""
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import time

from backend.models.base import get_db
from backend.models.user import User
from backend.models.rag import RAGConversation, RAGMessage
from backend.api.routes.auth import get_current_active_user
from backend.services.rag_service import RAGService
from backend.config.settings import settings

router = APIRouter()


# Pydantic schemas
class QueryRequest(BaseModel):
    query: str
    conversation_id: Optional[int] = None
    use_history: bool = True


class QueryResponse(BaseModel):
    response: str
    sources: List[dict]
    conversation_id: int
    message_id: int
    response_time_ms: int


class ConversationResponse(BaseModel):
    id: int
    title: Optional[str]
    message_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class MessageResponse(BaseModel):
    id: int
    role: str
    content: str
    sources: Optional[List[dict]]
    created_at: datetime

    class Config:
        from_attributes = True


class FeedbackRequest(BaseModel):
    message_id: int
    rating: int  # 1-5
    feedback: Optional[str] = None


# Initialize RAG service
rag_service = RAGService()


@router.post("/query", response_model=QueryResponse)
async def query_ai(
    query_request: QueryRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Submit a question to the AI assistant

    The AI will retrieve relevant information from the knowledge base
    and generate a comprehensive answer with citations.
    """
    start_time = time.time()

    # Get or create conversation
    if query_request.conversation_id:
        conversation = db.query(RAGConversation).filter(
            RAGConversation.id == query_request.conversation_id,
            RAGConversation.user_id == current_user.id
        ).first()
        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )
    else:
        # Create new conversation
        conversation = RAGConversation(
            user_id=current_user.id,
            title=query_request.query[:100]  # First 100 chars as title
        )
        db.add(conversation)
        db.commit()
        db.refresh(conversation)

    # Save user message
    user_message = RAGMessage(
        conversation_id=conversation.id,
        role="user",
        content=query_request.query
    )
    db.add(user_message)
    db.commit()

    try:
        # Get conversation history if requested
        history = []
        if query_request.use_history:
            previous_messages = db.query(RAGMessage).filter(
                RAGMessage.conversation_id == conversation.id
            ).order_by(RAGMessage.created_at.desc()).limit(10).all()
            history = [
                {"role": msg.role, "content": msg.content}
                for msg in reversed(previous_messages[:-1])  # Exclude the just-added user message
            ]

        # Query the RAG service
        result = await rag_service.query(
            query=query_request.query,
            conversation_history=history
        )

        # Save assistant message
        assistant_message = RAGMessage(
            conversation_id=conversation.id,
            role="assistant",
            content=result["response"],
            sources=result.get("sources"),
            similarity_scores=result.get("similarity_scores"),
            model_used=result.get("model_used", settings.OPENAI_MODEL),
            tokens_used=result.get("tokens_used"),
            response_time_ms=int((time.time() - start_time) * 1000)
        )
        db.add(assistant_message)

        # Update conversation
        conversation.message_count += 2  # User + assistant
        conversation.last_message_at = datetime.utcnow()
        db.commit()
        db.refresh(assistant_message)

        return QueryResponse(
            response=result["response"],
            sources=result.get("sources", []),
            conversation_id=conversation.id,
            message_id=assistant_message.id,
            response_time_ms=assistant_message.response_time_ms
        )

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing query: {str(e)}"
        )


@router.get("/conversations", response_model=List[ConversationResponse])
async def get_conversations(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
    limit: int = 20,
    offset: int = 0
):
    """Get user's conversation history"""
    conversations = db.query(RAGConversation).filter(
        RAGConversation.user_id == current_user.id
    ).order_by(RAGConversation.updated_at.desc()).offset(offset).limit(limit).all()

    return conversations


@router.get("/conversations/{conversation_id}/messages", response_model=List[MessageResponse])
async def get_conversation_messages(
    conversation_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get messages in a conversation"""
    conversation = db.query(RAGConversation).filter(
        RAGConversation.id == conversation_id,
        RAGConversation.user_id == current_user.id
    ).first()

    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )

    messages = db.query(RAGMessage).filter(
        RAGMessage.conversation_id == conversation_id
    ).order_by(RAGMessage.created_at).all()

    return [
        MessageResponse(
            id=msg.id,
            role=msg.role,
            content=msg.content,
            sources=msg.sources if msg.sources else None,
            created_at=msg.created_at
        )
        for msg in messages
    ]


@router.delete("/conversations/{conversation_id}")
async def delete_conversation(
    conversation_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete a conversation"""
    conversation = db.query(RAGConversation).filter(
        RAGConversation.id == conversation_id,
        RAGConversation.user_id == current_user.id
    ).first()

    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )

    db.delete(conversation)
    db.commit()

    return {"message": "Conversation deleted successfully"}


@router.post("/feedback")
async def submit_feedback(
    feedback: FeedbackRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Submit feedback on an AI response"""
    message = db.query(RAGMessage).join(RAGConversation).filter(
        RAGMessage.id == feedback.message_id,
        RAGConversation.user_id == current_user.id
    ).first()

    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found"
        )

    if not 1 <= feedback.rating <= 5:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Rating must be between 1 and 5"
        )

    message.user_rating = feedback.rating
    message.user_feedback = feedback.feedback
    db.commit()

    return {"message": "Feedback submitted successfully"}


@router.post("/documents/upload")
async def upload_document(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Upload a document to the knowledge base (admin only)

    Supported formats: PDF, DOCX, TXT, MD
    """
    if current_user.role not in ["admin", "instructor"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators and instructors can upload documents"
        )

    # Validate file type
    file_ext = file.filename.split(".")[-1].lower()
    if f".{file_ext}" not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type .{file_ext} not allowed. Allowed types: {settings.ALLOWED_EXTENSIONS}"
        )

    # Validate file size
    content = await file.read()
    if len(content) > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File too large. Maximum size: {settings.MAX_UPLOAD_SIZE / 1024 / 1024}MB"
        )

    try:
        # Process and embed document
        result = await rag_service.ingest_document(
            file_content=content,
            filename=file.filename,
            metadata={
                "uploaded_by": current_user.id,
                "upload_date": datetime.utcnow().isoformat()
            }
        )

        return {
            "message": "Document uploaded and processed successfully",
            "filename": file.filename,
            "chunks_created": result.get("chunks_created", 0),
            "document_id": result.get("document_id")
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing document: {str(e)}"
        )


@router.get("/stats")
async def get_rag_stats(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get RAG system statistics"""
    user_conversations = db.query(RAGConversation).filter(
        RAGConversation.user_id == current_user.id
    ).count()

    user_messages = db.query(RAGMessage).join(RAGConversation).filter(
        RAGConversation.user_id == current_user.id
    ).count()

    avg_rating = db.query(RAGMessage).join(RAGConversation).filter(
        RAGConversation.user_id == current_user.id,
        RAGMessage.user_rating.isnot(None)
    ).with_entities(func.avg(RAGMessage.user_rating)).scalar()

    return {
        "conversations": user_conversations,
        "messages": user_messages,
        "average_rating": float(avg_rating) if avg_rating else None
    }
