from typing import Any, Dict, Union

from sqlalchemy.ext.asyncio import AsyncSession
from .base import CRUDBase
from sql.models import Products
from schemas import ProductCreate, ProductUpdate


class CRUDProduct(CRUDBase[Products, ProductCreate, ProductUpdate]):

    async def create(self, db: AsyncSession, *, obj_in: ProductCreate) -> Products:
        db_obj = Products(
            name=obj_in.name,
            purchase_cost=obj_in.purchase_cost,
            selling_cost=obj_in.selling_cost,
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(
        self, db: AsyncSession, *, db_obj: Products, obj_in: Union[ProductUpdate, Dict[str, Any]]
    ) -> Products:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return await super().update(db, db_obj=db_obj, obj_in=update_data)


product = CRUDProduct(Products)
