from typing import Any, Dict, Union

from sqlalchemy.ext.asyncio import AsyncSession
from .base import CRUDBase
from sql.models import PurchaseRegistry
from schemas import PurchaseRegistryCreate, PurchaseRegistryUpdate


class CRUDPurchaseRegistry(CRUDBase[PurchaseRegistry, PurchaseRegistryCreate, PurchaseRegistryUpdate]):

    async def create(self, db: AsyncSession, *, obj_in: PurchaseRegistryCreate) -> PurchaseRegistry:
        db_obj = PurchaseRegistry(
            user_id=obj_in.user_id,
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(
        self, db: AsyncSession, *, db_obj: PurchaseRegistry, obj_in: Union[PurchaseRegistryUpdate, Dict[str, Any]]
    ) -> PurchaseRegistry:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return await super().update(db, db_obj=db_obj, obj_in=update_data)


purchase_registry = CRUDPurchaseRegistry(PurchaseRegistry)
