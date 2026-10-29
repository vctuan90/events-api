from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from app.models.session import SessionTypeEnum


# Base Session Schema
class SessionBase(BaseModel):
    title: str
    description: Optional[str] = None
    start_time: datetime
    end_time: datetime
    location: Optional[str] = None
    session_type: SessionTypeEnum = SessionTypeEnum.scheduled
    is_live: bool = False
    max_participants: Optional[int] = None


# Session Create Schema
class SessionCreate(SessionBase):
    event_id: int


# Session Update Schema
class SessionUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    location: Optional[str] = None
    session_type: Optional[SessionTypeEnum] = None
    is_live: Optional[bool] = None
    max_participants: Optional[int] = None


# Session Response Schema
class SessionResponse(SessionBase):
    id: int
    event_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# User Session Schemas
class UserSessionCreate(BaseModel):
    user_id: int
    session_id: int


class UserSessionResponse(BaseModel):
    id: int
    user_id: int
    session_id: int
    registered_at: datetime
    attended: bool = False

    class Config:
        from_attributes = True 