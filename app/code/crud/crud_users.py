from typing import Any, Dict, Union

from sqlalchemy.ext.asyncio import AsyncSession
from .base import CRUDBase,CRUDUpdate,CRUDDelete
from sql.models import Users
from schemas import  UserCreate, UserUpdate


class CRUDUser(CRUDBase[Users, UserCreate], CRUDUpdate[UserUpdate],CRUDDelete):

    async def update(
        self, db: AsyncSession, *, db_obj: Users, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> Users:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        return await super().update(db, db_obj=db_obj, obj_in=update_data)


user = CRUDUser(Users)

