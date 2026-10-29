from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user, get_current_admin_user
from app.models.user import User
from app.models.session import Session, UserSession
from app.schemas.session import (
    SessionCreate, SessionUpdate, SessionResponse,
    UserSessionCreate, UserSessionResponse
)
from app.crud.session import session_crud, user_session_crud

router = APIRouter()


@router.get("/", response_model=List[SessionResponse])
async def get_sessions(
    *,
    db: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    event_id: Optional[int] = Query(None)
) -> List[SessionResponse]:
    """Get all sessions"""
    if event_id:
        sessions = await session_crud.get_by_event(
            db, event_id=event_id, skip=skip, limit=limit
        )
    else:
        sessions = await session_crud.get_multi(db, skip=skip, limit=limit)
    return sessions


@router.get("/{session_id}", response_model=SessionResponse)
async def get_session(
    *,
    db: AsyncSession = Depends(get_db),
    session_id: int
) -> SessionResponse:
    """Get session by ID"""
    session = await session_crud.get(db, id=session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    return session


@router.post("/", response_model=SessionResponse, status_code=status.HTTP_201_CREATED)
async def create_session(
    *,
    db: AsyncSession = Depends(get_db),
    session_in: SessionCreate,
    current_user: User = Depends(get_current_admin_user)
) -> SessionResponse:
    """Create new session (Admin only)"""
    session = await session_crud.create(db, obj_in=session_in)
    return session


@router.put("/{session_id}", response_model=SessionResponse)
async def update_session(
    *,
    db: AsyncSession = Depends(get_db),
    session_id: int,
    session_in: SessionUpdate,
    current_user: User = Depends(get_current_admin_user)
) -> SessionResponse:
    """Update session (Admin only)"""
    session = await session_crud.get(db, id=session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    session = await session_crud.update(db, db_obj=session, obj_in=session_in)
    return session


@router.post("/{session_id}/register", response_model=UserSessionResponse)
async def register_for_session(
    *,
    db: AsyncSession = Depends(get_db),
    session_id: int,
    current_user: User = Depends(get_current_user)
) -> UserSessionResponse:
    """Register user for session"""
    # Check if session exists
    session = await session_crud.get(db, id=session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    # Check if already registered
    existing = await user_session_crud.get_by_user_and_session(
        db, user_id=current_user.id, session_id=session_id
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Already registered for this session"
        )
    
    # Register user
    user_session_data = UserSessionCreate(
        user_id=current_user.id,
        session_id=session_id
    )
    user_session = await user_session_crud.create(db, obj_in=user_session_data)
    return user_session


@router.delete("/{session_id}/register")
async def unregister_from_session(
    *,
    db: AsyncSession = Depends(get_db),
    session_id: int,
    current_user: User = Depends(get_current_user)
):
    """Unregister user from session"""
    user_session = await user_session_crud.get_by_user_and_session(
        db, user_id=current_user.id, session_id=session_id
    )
    if not user_session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not registered for this session"
        )
    
    await user_session_crud.remove(db, id=user_session.id)
    return {"message": "Successfully unregistered from session"}


@router.get("/{session_id}/participants")
async def get_session_participants(
    *,
    db: AsyncSession = Depends(get_db),
    session_id: int,
    current_user: User = Depends(get_current_admin_user),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100)
):
    """Get session participants (Admin only)"""
    session = await session_crud.get(db, id=session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    participants = await user_session_crud.get_session_participants(
        db, session_id=session_id, skip=skip, limit=limit
    )
    return participants 