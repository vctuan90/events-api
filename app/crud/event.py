from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from app.crud.base import CRUDBase
from app.models.event import Event
from app.schemas.event import EventCreate, EventUpdate


class CRUDEvent(CRUDBase[Event, EventCreate, EventUpdate]):
    async def get_multi(
        self,
        db: AsyncSession,
        *,
        skip: int = 0,
        limit: int = 100,
        is_active: Optional[bool] = None
    ) -> List[Event]:
        """Get multiple events with optional filtering"""
        stmt = select(Event)
        
        if is_active is not None:
            stmt = stmt.where(Event.is_active == is_active)
        
        stmt = stmt.offset(skip).limit(limit).order_by(Event.start_date.desc())
        
        result = await db.execute(stmt)
        return result.scalars().all()

    async def get_active_events(
        self, db: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> List[Event]:
        """Get only active events"""
        return await self.get_multi(
            db, skip=skip, limit=limit, is_active=True
        )

    async def get_upcoming_events(
        self, db: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> List[Event]:
        """Get upcoming active events"""
        from datetime import datetime
        
        stmt = select(Event).where(
            and_(
                Event.is_active == True,
                Event.start_date > datetime.utcnow()
            )
        ).offset(skip).limit(limit).order_by(Event.start_date.asc())
        
        result = await db.execute(stmt)
        return result.scalars().all()


event_crud = CRUDEvent(Event)