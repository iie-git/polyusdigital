from typing import Any, Dict, Union, List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .base import CRUDBase, ModelType
from sql.models import Purchases
from schemas import PurchaseCreate, PurchaseUpdate


class CRUDPurchase(CRUDBase[Purchases, PurchaseCreate, PurchaseUpdate]):
    async def create(self, db: AsyncSession, *, obj_in: PurchaseCreate) -> Purchases:
        db_obj = Purchases(
            registry_id = obj_in.registry_id,
            product_id = obj_in.product_id,
            count = obj_in.count
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(
        self, db: AsyncSession, *, db_obj: Purchases, obj_in: Union[PurchaseUpdate,Dict[str,Any]]
    ) -> Purchases:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return await super().update(db, db_obj=db_obj, obj_in=update_data)

    async def get_multi_by_filter(
            self, db: AsyncSession, *,filter_list: Any = None, skip: int = None, limit: int = None
    ) -> List[ModelType]:
        query = select(self.model).filter(*filter_list)
        if isinstance(skip, int) and skip > 0:
            query = query.offset(skip)
        if isinstance(limit, int) and limit > 0:
            query = query.limit(limit)
        result = await db.execute(query).scalar().all()
        return result


purchase = CRUDPurchase(Purchases)
