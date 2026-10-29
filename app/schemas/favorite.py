from pydantic import BaseModel
from datetime import datetime
from app.models.common import FavoritableTypeEnum


# Favorite Create Schema
class FavoriteCreate(BaseModel):
    favoritable_type: FavoritableTypeEnum
    favoritable_id: int


# Favorite Response Schema
class FavoriteResponse(BaseModel):
    id: int
    user_id: int
    favoritable_type: FavoritableTypeEnum
    favoritable_id: int
    created_at: datetime

    class Config:
        from_attributes = True 