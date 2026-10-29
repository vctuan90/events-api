from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime


# Base Speaker Schema
class SpeakerBase(BaseModel):
    first_name: str
    last_name: str
    title: Optional[str] = None
    company: Optional[str] = None
    bio: Optional[str] = None
    profile_image: Optional[str] = None
    email: Optional[EmailStr] = None
    linkedin: Optional[str] = None


# Speaker Create Schema
class SpeakerCreate(SpeakerBase):
    pass


# Speaker Update Schema
class SpeakerUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    title: Optional[str] = None
    company: Optional[str] = None
    bio: Optional[str] = None
    profile_image: Optional[str] = None
    email: Optional[EmailStr] = None
    linkedin: Optional[str] = None


# Speaker Response Schema
class SpeakerResponse(SpeakerBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True 