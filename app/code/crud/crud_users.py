from typing import Any, Dict, Union

from sqlalchemy.ext.asyncio import AsyncSession
from .base import CRUDBase
from sql.models import Users
from schemas import  UserCreate, UserUpdate


class CRUDUser(CRUDBase[Users, UserCreate, UserUpdate]):

    async def create(self, db: AsyncSession, *, obj_in: UserCreate) -> Users:
        db_obj = Users(
            full_name=obj_in.full_name,
            birth_year=obj_in.birth_year,
            gender=obj_in.gender.value,
            processing_consent=obj_in.processing_consent,
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(
        self, db: AsyncSession, *, db_obj: Users, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> Users:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        return await super().update(db, db_obj=db_obj, obj_in=update_data)


user = CRUDUser(Users)

