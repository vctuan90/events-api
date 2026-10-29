from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.common import Favorite, FavoritableTypeEnum
from app.schemas.favorite import FavoriteCreate, FavoriteResponse
from app.crud.favorite import favorite_crud

router = APIRouter()


@router.get("/", response_model=List[FavoriteResponse])
async def get_user_favorites(
    *,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    favoritable_type: FavoritableTypeEnum = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100)
) -> List[FavoriteResponse]:
    """Get user's favorites"""
    favorites = await favorite_crud.get_user_favorites(
        db, 
        user_id=current_user.id,
        favoritable_type=favoritable_type,
        skip=skip, 
        limit=limit
    )
    return favorites


@router.post("/", response_model=FavoriteResponse, status_code=status.HTTP_201_CREATED)
async def add_to_favorites(
    *,
    db: AsyncSession = Depends(get_db),
    favorite_in: FavoriteCreate,
    current_user: User = Depends(get_current_user)
) -> FavoriteResponse:
    """Add item to favorites"""
    # Check if already in favorites
    existing = await favorite_crud.get_user_favorite(
        db,
        user_id=current_user.id,
        favoritable_type=favorite_in.favoritable_type,
        favoritable_id=favorite_in.favoritable_id
    )
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Item already in favorites"
        )
    
    # Add user_id to the favorite data
    favorite_data = favorite_in.dict()
    favorite_data["user_id"] = current_user.id
    
    favorite = await favorite_crud.create(db, obj_in=favorite_data)
    return favorite


@router.delete("/{favorite_id}")
async def remove_from_favorites(
    *,
    db: AsyncSession = Depends(get_db),
    favorite_id: int,
    current_user: User = Depends(get_current_user)
):
    """Remove item from favorites"""
    favorite = await favorite_crud.get(db, id=favorite_id)
    if not favorite:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Favorite not found"
        )
    
    # Check if favorite belongs to current user
    if favorite.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to remove this favorite"
        )
    
    await favorite_crud.remove(db, id=favorite_id)
    return {"message": "Removed from favorites"}


@router.delete("/")
async def remove_favorite_by_item(
    *,
    db: AsyncSession = Depends(get_db),
    favoritable_type: FavoritableTypeEnum,
    favoritable_id: int,
    current_user: User = Depends(get_current_user)
):
    """Remove specific item from favorites"""
    favorite = await favorite_crud.get_user_favorite(
        db,
        user_id=current_user.id,
        favoritable_type=favoritable_type,
        favoritable_id=favoritable_id
    )
    
    if not favorite:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not in favorites"
        )
    
    await favorite_crud.remove(db, id=favorite.id)
    return {"message": "Removed from favorites"} 