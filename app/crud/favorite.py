from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from app.crud.base import CRUDBase
from app.models.common import Favorite, FavoritableTypeEnum
from app.schemas.favorite import FavoriteCreate


class CRUDFavorite(CRUDBase[Favorite, FavoriteCreate, dict]):
    async def get_user_favorites(
        self,
        db: AsyncSession,
        *,
        user_id: int,
        favoritable_type: Optional[FavoritableTypeEnum] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Favorite]:
        """Get user's favorites with optional type filtering"""
        stmt = select(Favorite).where(Favorite.user_id == user_id)
        
        if favoritable_type:
            stmt = stmt.where(Favorite.favoritable_type == favoritable_type)
        
        stmt = stmt.offset(skip).limit(limit).order_by(Favorite.created_at.desc())
        
        result = await db.execute(stmt)
        return result.scalars().all()

    async def get_user_favorite(
        self,
        db: AsyncSession,
        *,
        user_id: int,
        favoritable_type: FavoritableTypeEnum,
        favoritable_id: int
    ) -> Optional[Favorite]:
        """Get specific user favorite"""
        stmt = select(Favorite).where(
            and_(
                Favorite.user_id == user_id,
                Favorite.favoritable_type == favoritable_type,
                Favorite.favoritable_id == favoritable_id
            )
        )
        
        result = await db.execute(stmt)
        return result.scalar_one_or_none()


favorite_crud = CRUDFavorite(Favorite) 