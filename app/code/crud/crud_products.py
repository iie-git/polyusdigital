from typing import Any, Dict, Union

from sqlalchemy.ext.asyncio import AsyncSession
from .base import CRUDBase, CRUDUpdate, CRUDDelete
from sql.models import Products
from schemas import ProductCreate, ProductUpdate


class CRUDProduct(CRUDBase[Products, ProductCreate], CRUDUpdate[ProductUpdate], CRUDDelete):

    async def update(
        self, db: AsyncSession, *, db_obj: Products, obj_in: Union[ProductUpdate, Dict[str, Any]]
    ) -> Products:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return await super().update(db, db_obj=db_obj, obj_in=update_data)


product = CRUDProduct(Products)
