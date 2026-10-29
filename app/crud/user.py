from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_

from app.crud.base import CRUDBase
from app.models.user import User, UserRole
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash, verify_password, generate_qr_code_token


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    async def get_by_email(self, db: AsyncSession, *, email: str) -> Optional[User]:
        """Get user by email"""
        stmt = select(User).where(User.email == email)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_qr_code(self, db: AsyncSession, *, qr_code: str) -> Optional[User]:
        """Get user by QR code"""
        stmt = select(User).where(User.qr_code == qr_code)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, db: AsyncSession, *, obj_in: UserCreate) -> User:
        """Create user with hashed password and QR code"""
        # Hash password
        hashed_password = get_password_hash(obj_in.password)
        
        # Generate unique QR code
        qr_code = generate_qr_code_token()
        while await self.get_by_qr_code(db, qr_code=qr_code):
            qr_code = generate_qr_code_token()
        
        # Create user object
        db_obj = User(
            email=obj_in.email,
            password_hash=hashed_password,
            full_name=obj_in.full_name,
            is_active=obj_in.is_active,
            role=obj_in.role,
            qr_code=qr_code
        )
        
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def authenticate(self, db: AsyncSession, *, email: str, password: str) -> Optional[User]:
        """Authenticate user with email and password"""
        user = await self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.password_hash):
            return None
        return user

    async def is_active(self, user: User) -> bool:
        """Check if user is active"""
        return user.is_active

    async def is_admin(self, user: User) -> bool:
        """Check if user is admin"""
        return user.role == UserRole.ADMIN

    async def update_password(self, db: AsyncSession, *, user: User, new_password: str) -> User:
        """Update user password"""
        hashed_password = get_password_hash(new_password)
        user.password_hash = hashed_password
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

    async def activate_user(self, db: AsyncSession, *, user: User) -> User:
        """Activate user account"""
        user.is_active = True
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

    async def deactivate_user(self, db: AsyncSession, *, user: User) -> User:
        """Deactivate user account"""
        user.is_active = False
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

    async def make_admin(self, db: AsyncSession, *, user: User) -> User:
        """Make user admin"""
        user.role = UserRole.ADMIN
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

    async def remove_admin(self, db: AsyncSession, *, user: User) -> User:
        """Remove admin privileges"""
        user.role = UserRole.ATTENDEE
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

    async def search_users(
        self, 
        db: AsyncSession, 
        *, 
        query: str, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[User]:
        """Search users by name, email, or company"""
        search_term = f"%{query.lower()}%"
        
        stmt = select(User).where(
            or_(
                User.full_name.ilike(search_term),
                User.email.ilike(search_term),
                User.company.ilike(search_term)
            )
        ).where(User.is_active == True).offset(skip).limit(limit)
        
        result = await db.execute(stmt)
        return result.scalars().all()

    async def get_users_for_networking(
        self, 
        db: AsyncSession, 
        *, 
        current_user_id: str,
        skip: int = 0, 
        limit: int = 100,
        search: Optional[str] = None
    ) -> List[User]:
        """Get users for networking (excluding current user)"""
        stmt = select(User).where(
            User.id != current_user_id,
            User.is_active == True
        )
        
        if search:
            search_term = f"%{search.lower()}%"
            stmt = stmt.where(
                or_(
                    User.full_name.ilike(search_term),
                    User.company.ilike(search_term),
                    User.position.ilike(search_term)
                )
            )
        
        stmt = stmt.offset(skip).limit(limit).order_by(User.full_name)
        
        result = await db.execute(stmt)
        return result.scalars().all()

    async def get_admins(self, db: AsyncSession, *, skip: int = 0, limit: int = 100) -> List[User]:
        """Get all admin users"""
        stmt = select(User).where(
            User.role == UserRole.ADMIN,
            User.is_active == True
        ).offset(skip).limit(limit)
        
        result = await db.execute(stmt)
        return result.scalars().all()


user_crud = CRUDUser(User) 