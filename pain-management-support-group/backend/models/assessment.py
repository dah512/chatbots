"""
Assessment models for pre/post tests and quizzes
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float, Boolean, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from .base import Base


class AssessmentType(str, enum.Enum):
    """Assessment type enumeration"""
    PRE_TEST = "pre_test"
    POST_TEST = "post_test"
    QUIZ = "quiz"
    FUNCTIONAL = "functional"


class QuestionType(str, enum.Enum):
    """Question type enumeration"""
    MULTIPLE_CHOICE = "multiple_choice"
    TRUE_FALSE = "true_false"
    SHORT_ANSWER = "short_answer"
    SCALE = "scale"  # For pain scales, satisfaction, etc.


class Assessment(Base):
    """Assessment container (pre-test, post-test, quiz)"""
    __tablename__ = "assessments"

    id = Column(Integer, primary_key=True, index=True)
    week_id = Column(Integer, ForeignKey("weeks.id"), nullable=False)

    title = Column(String(300), nullable=False)
    description = Column(Text, nullable=True)
    assessment_type = Column(SQLEnum(AssessmentType), nullable=False)

    # Scoring
    total_points = Column(Integer, nullable=False)
    passing_score = Column(Float, nullable=False)  # Percentage

    # Timing
    time_limit_minutes = Column(Integer, nullable=True)
    is_timed = Column(Boolean, default=False)

    # Availability
    is_published = Column(Boolean, default=False)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    week = relationship("Week", back_populates="assessments")
    questions = relationship("AssessmentQuestion", back_populates="assessment", cascade="all, delete-orphan")
    submissions = relationship("AssessmentSubmission", back_populates="assessment", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Assessment(id={self.id}, type='{self.assessment_type}', week={self.week_id})>"


class AssessmentQuestion(Base):
    """Individual question within an assessment"""
    __tablename__ = "assessment_questions"

    id = Column(Integer, primary_key=True, index=True)
    assessment_id = Column(Integer, ForeignKey("assessments.id"), nullable=False)

    question_text = Column(Text, nullable=False)
    question_type = Column(SQLEnum(QuestionType), nullable=False)
    points = Column(Integer, default=1, nullable=False)
    sequence_order = Column(Integer, nullable=False)

    # Multiple choice options
    options = Column(Text, nullable=True)  # JSON string: {"A": "...", "B": "...", etc.}
    correct_answer = Column(String(500), nullable=False)  # For MC: "A", for scale: "7", etc.

    # Explanation
    explanation = Column(Text, nullable=True)

    # Visual aids
    image_url = Column(String(500), nullable=True)
    diagram_url = Column(String(500), nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    assessment = relationship("Assessment", back_populates="questions")
    answers = relationship("AssessmentAnswer", back_populates="question", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<AssessmentQuestion(id={self.id}, type='{self.question_type}')>"


class AssessmentSubmission(Base):
    """User's submission of an assessment"""
    __tablename__ = "assessment_submissions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    assessment_id = Column(Integer, ForeignKey("assessments.id"), nullable=False)

    # Scoring
    score = Column(Float, nullable=False)  # Points earned
    percentage = Column(Float, nullable=False)  # Percentage score
    passed = Column(Boolean, nullable=False)

    # Timing
    started_at = Column(DateTime(timezone=True), nullable=False)
    submitted_at = Column(DateTime(timezone=True), nullable=False)
    time_taken_minutes = Column(Integer, nullable=True)

    # Completion
    is_complete = Column(Boolean, default=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="assessment_submissions")
    assessment = relationship("Assessment", back_populates="submissions")
    answers = relationship("AssessmentAnswer", back_populates="submission", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<AssessmentSubmission(id={self.id}, user={self.user_id}, score={self.percentage}%)>"


class AssessmentAnswer(Base):
    """Individual answer within a submission"""
    __tablename__ = "assessment_answers"

    id = Column(Integer, primary_key=True, index=True)
    submission_id = Column(Integer, ForeignKey("assessment_submissions.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("assessment_questions.id"), nullable=False)

    user_answer = Column(Text, nullable=False)
    is_correct = Column(Boolean, nullable=False)
    points_earned = Column(Integer, nullable=False)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    submission = relationship("AssessmentSubmission", back_populates="answers")
    question = relationship("AssessmentQuestion", back_populates="answers")

    def __repr__(self):
        return f"<AssessmentAnswer(id={self.id}, correct={self.is_correct})>"
