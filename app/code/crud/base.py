from typing import Any, Generic, List, Optional, Type, TypeVar

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


ModelType = TypeVar("ModelType", bound=Any)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    async def get(self, db: AsyncSession, id: Any) -> Optional[ModelType]:

        query = select(self.model).filter(self.model.id == id)
        result = await db.execute(query)
        return result.scalars().first()

    async def get_multi(
        self, db: AsyncSession, *, skip: int = None, limit: int = None
    ) -> List[ModelType]:
        query = select(self.model)
        if isinstance(skip,int) and skip > 0:
            query=query.offset(skip)
        if isinstance(limit, int) and limit > 0:
            query = query.limit(limit)
        result = await db.execute(query)
        return result.scalars().all()

    async def get_multi_by_filter(
            self, db: AsyncSession, *,filter_list: Any = None, skip: int = None, limit: int = None
    ) -> List[ModelType]:
        query = select(self.model).filter(*filter_list)
        if isinstance(skip, int) and skip > 0:
            query = query.offset(skip)
        if isinstance(limit, int) and limit > 0:
            query = query.limit(limit)
        result = await db.execute(query)
        return result.scalars().all()

    async def create(self, db: AsyncSession, *, obj_in: CreateSchemaType) -> ModelType:
        db_obj = self.model(**obj_in.model_dump())
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj


class CRUDUpdate(Generic[UpdateSchemaType]):
    async def update(
        self,
        db: AsyncSession,
        *,
        db_obj: ModelType,
        obj_in: UpdateSchemaType
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

class CRUDDelete():

    async def delete(self, db: AsyncSession, *, model_item: ModelType) -> bool:
        await db.delete(model_item)
        await db.commit()
        return True
