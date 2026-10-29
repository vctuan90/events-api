from sqlalchemy import Column, String, DateTime, Text, ForeignKey, Enum, Integer
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum

from app.core.database import Base


class SessionSpeakerRoleEnum(str, enum.Enum):
    speaker = "speaker"
    moderator = "moderator"
    panelist = "panelist"


class Speaker(Base):
    __tablename__ = "speakers"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    title = Column(String(255))
    company = Column(String(255))
    bio = Column(Text)
    profile_image = Column(Text)
    email = Column(String(255))
    linkedin = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    session_speakers = relationship("SessionSpeaker", back_populates="speaker")

    @property
    def full_name(self) -> str:
        """Get speaker's full name"""
        return f"{self.first_name} {self.last_name}"

    def __repr__(self):
        return f"<Speaker {self.full_name}>"


class SessionSpeaker(Base):
    __tablename__ = "session_speakers"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False)
    speaker_id = Column(Integer, ForeignKey("speakers.id"), nullable=False)
    role = Column(Enum(SessionSpeakerRoleEnum), default=SessionSpeakerRoleEnum.speaker)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    session = relationship("Session", back_populates="session_speakers")
    speaker = relationship("Speaker", back_populates="session_speakers")

    def __repr__(self):
        return f"<SessionSpeaker {self.session_id} - {self.speaker_id}>" 