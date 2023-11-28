from typing import Any, List, Annotated
from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy import func, desc, cast, Date, select
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from api import deps
from sql.models import Purchases, PurchaseRegistry, Users, Products

router = APIRouter()
SessionInstance = Annotated[AsyncSession, Depends(deps.get_session)]


class ReportUserOrdersCost(BaseModel):
    full_name: str
    purchases_cost: float


@router.get("/users/by/purchases_cost", response_model=List[ReportUserOrdersCost])
async def read_products(
    db: SessionInstance,
    purchase_date: date = None
) -> Any:
    """
    Получение отчета по пользователям  относительно стоимости их покупок.
    """
    query = select(Users.full_name, func.sum(Purchases.total_cost).label('purchases_cost'))\
        .join(PurchaseRegistry, PurchaseRegistry.user_id == Users.id)\
        .join(Purchases, Purchases.registry_id == PurchaseRegistry.id)
    if purchase_date:
        query=query.filter(cast(PurchaseRegistry.purchase_date,Date) == purchase_date)
    query = query\
        .group_by(Users.id)\
        .order_by(desc('purchases_cost'))
    user_orders_cost = await db.execute(query)
    return user_orders_cost.all()

