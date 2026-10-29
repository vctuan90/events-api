from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import create_access_token, create_refresh_token, verify_token
from app.core.dependencies import get_current_user, get_current_active_user
from app.crud.user import user_crud
from app.schemas.user import (
    UserCreate, 
    UserResponse, 
    Token, 
    UserLogin
)
from app.models.user import User as UserModel

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    *,
    db: AsyncSession = Depends(get_db),
    user_in: UserCreate,
) -> UserResponse:
    """
    Register a new user
    """
    # Check if user already exists
    user = await user_crud.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
    
    # Create new user
    user = await user_crud.create(db, obj_in=user_in)
    return user


@router.post("/login", response_model=Token)
async def login(
    db: AsyncSession = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Token:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = await user_crud.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    elif not user_crud.is_active(user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="User account is disabled"
        )
    
    # Create tokens
    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)
    
    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )


@router.post("/login/json", response_model=Token)
async def login_json(
    *,
    db: AsyncSession = Depends(get_db),
    user_credentials: UserLogin
) -> Token:
    """
    JSON login endpoint
    """
    user = await user_crud.authenticate(
        db, email=user_credentials.email, password=user_credentials.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    elif not user_crud.is_active(user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is disabled"
        )
    
    # Create tokens
    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)
    
    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )


@router.post("/refresh", response_model=Token)
async def refresh_token(
    *,
    db: AsyncSession = Depends(get_db),
    refresh_token: str
) -> Token:
    """
    Refresh access token using refresh token
    """
    user_id = verify_token(refresh_token, token_type="refresh")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    user = await user_crud.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if not user_crud.is_active(user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is disabled"
        )
    
    # Create new tokens
    access_token = create_access_token(user.id)
    new_refresh_token = create_refresh_token(user.id)
    
    return Token(
        access_token=access_token,
        refresh_token=new_refresh_token,
        token_type="bearer"
    )


@router.post("/test-token", response_model=UserResponse)
async def test_token(current_user: UserModel = Depends(get_current_user)) -> UserResponse:
    """
    Test access token
    """
    return current_user


@router.post("/logout")
async def logout(
    current_user: UserModel = Depends(get_current_active_user)
):
    """
    Logout user (client-side token removal)
    """
    return {"message": "Successfully logged out"}


@router.post("/password-reset-request")
async def password_reset_request(
    *,
    db: AsyncSession = Depends(get_db),
    email: str
):
    """
    Request password reset
    """
    user = await user_crud.get_by_email(db, email=email)
    if not user:
        # Don't reveal if email exists or not
        return {"message": "If the email exists, password reset instructions have been sent"}
    
    # TODO: Send password reset email
    # This would typically involve:
    # 1. Generate password reset token
    # 2. Send email with reset link
    # 3. Store token temporarily (Redis/Database)
    
    return {"message": "If the email exists, password reset instructions have been sent"}


@router.post("/password-reset")
async def password_reset(
    *,
    db: AsyncSession = Depends(get_db),
    token: str,
    new_password: str
):
    """
    Reset password using reset token
    """
    # TODO: Verify password reset token
    # This would typically involve:
    # 1. Verify reset token
    # 2. Get user from token
    # 3. Update password
    
    # For now, return not implemented
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Password reset functionality not implemented yet"
    )


@router.get("/me", response_model=UserResponse)
async def read_users_me(
    current_user: UserModel = Depends(get_current_active_user)
) -> UserResponse:
    """
    Get current user
    """
    return current_user 