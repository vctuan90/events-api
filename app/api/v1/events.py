from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user, get_current_admin_user
from app.models.user import User
from app.models.event import Event
from app.schemas.event import EventCreate, EventUpdate, EventResponse
from app.crud.event import event_crud

router = APIRouter()


@router.get("/", response_model=List[EventResponse])
async def get_events(
    *,
    db: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    is_active: Optional[bool] = Query(None)
) -> List[EventResponse]:
    """Get all events"""
    events = await event_crud.get_multi(
        db, skip=skip, limit=limit, is_active=is_active
    )
    return events


@router.get("/{event_id}", response_model=EventResponse)
async def get_event(
    *,
    db: AsyncSession = Depends(get_db),
    event_id: int
) -> EventResponse:
    """Get event by ID"""
    event = await event_crud.get(db, id=event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    return event


@router.post("/", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
async def create_event(
    *,
    db: AsyncSession = Depends(get_db),
    event_in: EventCreate,
    current_user: User = Depends(get_current_admin_user)
) -> EventResponse:
    """Create new event (Admin only)"""
    event = await event_crud.create(db, obj_in=event_in)
    return event


@router.put("/{event_id}", response_model=EventResponse)
async def update_event(
    *,
    db: AsyncSession = Depends(get_db),
    event_id: int,
    event_in: EventUpdate,
    current_user: User = Depends(get_current_admin_user)
) -> EventResponse:
    """Update event (Admin only)"""
    event = await event_crud.get(db, id=event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    
    event = await event_crud.update(db, db_obj=event, obj_in=event_in)
    return event


@router.delete("/{event_id}")
async def delete_event(
    *,
    db: AsyncSession = Depends(get_db),
    event_id: int,
    current_user: User = Depends(get_current_admin_user)
):
    """Delete event (Admin only)"""
    event = await event_crud.get(db, id=event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    
    await event_crud.remove(db, id=event_id)
    return {"message": "Event deleted successfully"}


@router.get("/{event_id}/sessions")
async def get_event_sessions(
    *,
    db: AsyncSession = Depends(get_db),
    event_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100)
):
    """Get all sessions for an event"""
    event = await event_crud.get(db, id=event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    
    # Import here to avoid circular imports
    from app.crud.session import session_crud
    sessions = await session_crud.get_by_event(
        db, event_id=event_id, skip=skip, limit=limit
    )
    return sessions 