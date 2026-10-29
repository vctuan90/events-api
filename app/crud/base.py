from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, update, delete
from sqlalchemy.orm import selectinload
from fastapi.encoders import jsonable_encoder

from app.core.database import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        
        **Parameters**
        
        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    async def get(self, db: AsyncSession, id: Any) -> Optional[ModelType]:
        """Get a single record by id"""
        stmt = select(self.model).where(self.model.id == id)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_multi(
        self, 
        db: AsyncSession, 
        *, 
        skip: int = 0, 
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None,
        order_by: Optional[str] = None
    ) -> List[ModelType]:
        """Get multiple records with pagination and filtering"""
        stmt = select(self.model)
        
        # Apply filters
        if filters:
            for key, value in filters.items():
                if hasattr(self.model, key) and value is not None:
                    stmt = stmt.where(getattr(self.model, key) == value)
        
        # Apply ordering
        if order_by and hasattr(self.model, order_by):
            stmt = stmt.order_by(getattr(self.model, order_by))
        
        # Apply pagination
        stmt = stmt.offset(skip).limit(limit)
        
        result = await db.execute(stmt)
        return result.scalars().all()

    async def get_count(
        self, 
        db: AsyncSession,
        filters: Optional[Dict[str, Any]] = None
    ) -> int:
        """Get total count of records with optional filtering"""
        stmt = select(func.count(self.model.id))
        
        # Apply filters
        if filters:
            for key, value in filters.items():
                if hasattr(self.model, key) and value is not None:
                    stmt = stmt.where(getattr(self.model, key) == value)
        
        result = await db.execute(stmt)
        return result.scalar()

    async def create(self, db: AsyncSession, *, obj_in: CreateSchemaType) -> ModelType:
        """Create a new record"""
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(
        self,
        db: AsyncSession,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        """Update a record"""
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def delete(self, db: AsyncSession, *, id: Any) -> Optional[ModelType]:
        """Delete a record by id"""
        obj = await self.get(db, id=id)
        if obj:
            await db.delete(obj)
            await db.commit()
        return obj

    async def get_by_field(
        self, 
        db: AsyncSession, 
        field_name: str, 
        field_value: Any
    ) -> Optional[ModelType]:
        """Get a single record by any field"""
        if not hasattr(self.model, field_name):
            return None
        
        stmt = select(self.model).where(getattr(self.model, field_name) == field_value)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_multi_by_field(
        self, 
        db: AsyncSession, 
        field_name: str, 
        field_value: Any,
        skip: int = 0,
        limit: int = 100
    ) -> List[ModelType]:
        """Get multiple records by any field"""
        if not hasattr(self.model, field_name):
            return []
        
        stmt = select(self.model).where(
            getattr(self.model, field_name) == field_value
        ).offset(skip).limit(limit)
        
        result = await db.execute(stmt)
        return result.scalars().all()

    async def exists(self, db: AsyncSession, id: Any) -> bool:
        """Check if a record exists by id"""
        stmt = select(func.count(self.model.id)).where(self.model.id == id)
        result = await db.execute(stmt)
        count = result.scalar()
        return count > 0

    async def bulk_create(
        self, 
        db: AsyncSession, 
        *, 
        objs_in: List[CreateSchemaType]
    ) -> List[ModelType]:
        """Create multiple records"""
        db_objs = []
        for obj_in in objs_in:
            obj_in_data = jsonable_encoder(obj_in)
            db_obj = self.model(**obj_in_data)
            db_objs.append(db_obj)
        
        db.add_all(db_objs)
        await db.commit()
        
        for db_obj in db_objs:
            await db.refresh(db_obj)
        
        return db_objs

    async def bulk_update(
        self,
        db: AsyncSession,
        *,
        filters: Dict[str, Any],
        update_data: Dict[str, Any]
    ) -> int:
        """Bulk update records"""
        stmt = update(self.model)
        
        # Apply filters
        for key, value in filters.items():
            if hasattr(self.model, key):
                stmt = stmt.where(getattr(self.model, key) == value)
        
        # Apply updates
        stmt = stmt.values(**update_data)
        
        result = await db.execute(stmt)
        await db.commit()
        return result.rowcount

    async def bulk_delete(
        self,
        db: AsyncSession,
        *,
        filters: Dict[str, Any]
    ) -> int:
        """Bulk delete records"""
        stmt = delete(self.model)
        
        # Apply filters
        for key, value in filters.items():
            if hasattr(self.model, key):
                stmt = stmt.where(getattr(self.model, key) == value)
        
        result = await db.execute(stmt)
        await db.commit()
        return result.rowcount 