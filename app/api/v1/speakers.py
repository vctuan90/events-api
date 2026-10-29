from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_admin_user
from app.models.user import User
from app.models.speaker import Speaker
from app.schemas.speaker import SpeakerCreate, SpeakerUpdate, SpeakerResponse
from app.crud.speaker import speaker_crud

router = APIRouter()


@router.get("/", response_model=List[SpeakerResponse])
async def get_speakers(
    *,
    db: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100)
) -> List[SpeakerResponse]:
    """Get all speakers"""
    speakers = await speaker_crud.get_multi(db, skip=skip, limit=limit)
    return speakers


@router.get("/{speaker_id}", response_model=SpeakerResponse)
async def get_speaker(
    *,
    db: AsyncSession = Depends(get_db),
    speaker_id: int
) -> SpeakerResponse:
    """Get speaker by ID"""
    speaker = await speaker_crud.get(db, id=speaker_id)
    if not speaker:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Speaker not found"
        )
    return speaker


@router.post("/", response_model=SpeakerResponse, status_code=status.HTTP_201_CREATED)
async def create_speaker(
    *,
    db: AsyncSession = Depends(get_db),
    speaker_in: SpeakerCreate,
    current_user: User = Depends(get_current_admin_user)
) -> SpeakerResponse:
    """Create new speaker (Admin only)"""
    speaker = await speaker_crud.create(db, obj_in=speaker_in)
    return speaker


@router.put("/{speaker_id}", response_model=SpeakerResponse)
async def update_speaker(
    *,
    db: AsyncSession = Depends(get_db),
    speaker_id: int,
    speaker_in: SpeakerUpdate,
    current_user: User = Depends(get_current_admin_user)
) -> SpeakerResponse:
    """Update speaker (Admin only)"""
    speaker = await speaker_crud.get(db, id=speaker_id)
    if not speaker:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Speaker not found"
        )
    
    speaker = await speaker_crud.update(db, db_obj=speaker, obj_in=speaker_in)
    return speaker


@router.delete("/{speaker_id}")
async def delete_speaker(
    *,
    db: AsyncSession = Depends(get_db),
    speaker_id: int,
    current_user: User = Depends(get_current_admin_user)
):
    """Delete speaker (Admin only)"""
    speaker = await speaker_crud.get(db, id=speaker_id)
    if not speaker:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Speaker not found"
        )
    
    await speaker_crud.remove(db, id=speaker_id)
    return {"message": "Speaker deleted successfully"} 