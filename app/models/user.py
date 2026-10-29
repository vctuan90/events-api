from sqlalchemy import Column, String, Boolean, DateTime, Text, Enum, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
import enum

from app.core.database import Base


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    ORGANIZER = "organizer"
    SPEAKER = "speaker"
    ATTENDEE = "attendee"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    first_name = Column(String(100))
    last_name = Column(String(100))
    phone = Column(String(20))
    company = Column(String(255))
    position = Column(String(255))
    qr_code = Column(String(255), unique=True, index=True)
    profile_image = Column(Text)
    is_active = Column(Boolean, default=True)
    role = Column(Enum(UserRole), default=UserRole.ATTENDEE)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    sessions = relationship("UserSession", back_populates="user")
    favorites = relationship("Favorite", back_populates="user")
    questions = relationship("SessionQuestion", back_populates="user", foreign_keys="SessionQuestion.user_id")
    feedback = relationship("SessionFeedback", back_populates="user")
    notifications = relationship("Notification", back_populates="user")
    gallery_items = relationship("Gallery", back_populates="user")
    survey_responses = relationship("SurveyResponse", back_populates="user")
    user_badges = relationship("UserBadge", back_populates="user")
    digital_certificates = relationship("DigitalCertificate", back_populates="user")
    
    # Networking relationships
    sent_connections = relationship("NetworkingConnection", foreign_keys="NetworkingConnection.requester_id", back_populates="requester")
    received_connections = relationship("NetworkingConnection", foreign_keys="NetworkingConnection.requestee_id", back_populates="requestee")

    def __repr__(self):
        return f"<User {self.email}>" 