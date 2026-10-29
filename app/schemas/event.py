from typing import Optional
from pydantic import BaseModel
from datetime import datetime


# Base Event Schema
class EventBase(BaseModel):
    title: str
    description: Optional[str] = None
    start_date: datetime
    end_date: datetime
    location: Optional[str] = None
    banner_image: Optional[str] = None
    is_active: bool = True


# Event Create Schema
class EventCreate(EventBase):
    pass


# Event Update Schema
class EventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    location: Optional[str] = None
    banner_image: Optional[str] = None
    is_active: Optional[bool] = None


# Event Response Schema
class EventResponse(EventBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True 