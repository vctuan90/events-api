from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.core.database import get_db
from app.core.security import verify_token, TokenValidationError, InsufficientPermissionsError
from app.crud.user import user_crud
from app.models.user import User, UserRole

# JWT Bearer token scheme
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> User:
    """Get current authenticated user"""
    try:
        user_id = verify_token(credentials.credentials)
        if user_id is None:
            raise TokenValidationError()
        
        user = await user_crud.get(db, id=user_id)
        if user is None:
            raise TokenValidationError("User not found")
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is disabled"
            )
        
        return user
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise TokenValidationError()


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """Get current active user"""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is disabled"
        )
    return current_user


async def get_current_admin_user(
    current_user: User = Depends(get_current_active_user)
) -> User:
    """Get current admin user"""
    if current_user.role != UserRole.ADMIN:
        raise InsufficientPermissionsError("Admin access required")
    return current_user


async def get_optional_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> Optional[User]:
    """Get current user if token is provided, otherwise return None"""
    if credentials is None:
        return None
    
    try:
        user_id = verify_token(credentials.credentials)
        if user_id is None:
            return None
        
        user = await user_crud.get(db, id=user_id)
        if user is None or not user.is_active:
            return None
        
        return user
    except Exception:
        return None


def get_pagination_params(
    page: int = 1,
    per_page: int = 20
) -> tuple[int, int]:
    """Get pagination parameters with validation"""
    if page < 1:
        page = 1
    if per_page < 1:
        per_page = 20
    if per_page > 100:
        per_page = 100
    
    return page, per_page


def get_skip_limit(page: int, per_page: int) -> tuple[int, int]:
    """Convert page/per_page to skip/limit"""
    skip = (page - 1) * per_page
    limit = per_page
    return skip, limit 