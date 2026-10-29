from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from app.crud.base import CRUDBase
from app.models.session import Session, UserSession
from app.schemas.session import SessionCreate, SessionUpdate, UserSessionCreate


class CRUDSession(CRUDBase[Session, SessionCreate, SessionUpdate]):
    async def get_by_event(
        self,
        db: AsyncSession,
        *,
        event_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[Session]:
        """Get sessions by event ID"""
        stmt = select(Session).where(
            Session.event_id == event_id
        ).offset(skip).limit(limit).order_by(Session.start_time.asc())
        
        result = await db.execute(stmt)
        return result.scalars().all()

    async def get_live_sessions(
        self, db: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> List[Session]:
        """Get currently live sessions"""
        stmt = select(Session).where(
            Session.is_live == True
        ).offset(skip).limit(limit).order_by(Session.start_time.asc())
        
        result = await db.execute(stmt)
        return result.scalars().all()


class CRUDUserSession(CRUDBase[UserSession, UserSessionCreate, dict]):
    async def get_by_user_and_session(
        self,
        db: AsyncSession,
        *,
        user_id: int,
        session_id: int
    ) -> Optional[UserSession]:
        """Get user session registration"""
        stmt = select(UserSession).where(
            and_(
                UserSession.user_id == user_id,
                UserSession.session_id == session_id
            )
        )
        
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_user_sessions(
        self,
        db: AsyncSession,
        *,
        user_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[UserSession]:
        """Get all sessions for a user"""
        stmt = select(UserSession).where(
            UserSession.user_id == user_id
        ).offset(skip).limit(limit).order_by(UserSession.registered_at.desc())
        
        result = await db.execute(stmt)
        return result.scalars().all()

    async def get_session_participants(
        self,
        db: AsyncSession,
        *,
        session_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[UserSession]:
        """Get all participants for a session"""
        stmt = select(UserSession).where(
            UserSession.session_id == session_id
        ).offset(skip).limit(limit).order_by(UserSession.registered_at.asc())
        
        result = await db.execute(stmt)
        return result.scalars().all()


session_crud = CRUDSession(Session)
user_session_crud = CRUDUserSession(UserSession) 