from sqlalchemy import Column, String, Boolean, DateTime, Text, Integer, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum

from app.core.database import Base


class SessionTypeEnum(str, enum.Enum):
    live = "live"
    scheduled = "scheduled"
    workshop = "workshop"


class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=False)
    location = Column(String(255))
    session_type = Column(Enum(SessionTypeEnum), default=SessionTypeEnum.scheduled)
    is_live = Column(Boolean, default=False)
    max_participants = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    event = relationship("Event", back_populates="sessions")
    session_speakers = relationship("SessionSpeaker", back_populates="session")
    user_sessions = relationship("UserSession", back_populates="session")
    questions = relationship("SessionQuestion", back_populates="session")
    feedback = relationship("SessionFeedback", back_populates="session")

    def __repr__(self):
        return f"<Session {self.title}>"


class UserSession(Base):
    __tablename__ = "user_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False)
    registered_at = Column(DateTime(timezone=True), server_default=func.now())
    attended = Column(Boolean, default=False)

    # Relationships
    user = relationship("User", back_populates="sessions")
    session = relationship("Session", back_populates="user_sessions")

    def __repr__(self):
        return f"<UserSession {self.user_id} - {self.session_id}>"


class SessionQuestion(Base):
    __tablename__ = "session_questions"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    question = Column(Text, nullable=False)
    is_answered = Column(Boolean, default=False)
    answer = Column(Text)
    answered_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    session = relationship("Session", back_populates="questions")
    user = relationship("User", back_populates="questions", foreign_keys=[user_id])
    admin = relationship("User", foreign_keys=[answered_by])

    def __repr__(self):
        return f"<SessionQuestion {self.id}>"


class SessionFeedback(Base):
    __tablename__ = "session_feedback"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    rating = Column(Integer, nullable=False)  # 1-5 scale
    comment = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    session = relationship("Session", back_populates="feedback")
    user = relationship("User", back_populates="feedback")

    def __repr__(self):
        return f"<SessionFeedback {self.id}>" 