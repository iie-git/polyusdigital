from typing import Any, List, Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import UUID4

import schemas
from crud import purchase as purchase_crud
from crud import purchase_registry as purchase_registry_crud
from crud import check_by_id
from crud import product as product_crud
from api import deps
from sql.models import Purchases, Products


router = APIRouter()
SessionInstance = Annotated[AsyncSession, Depends(deps.get_session)]


@router.get("/", response_model=List[schemas.PurchaseItem])
async def read_purchase(
    db: SessionInstance,
    skip: int = None,
    limit: int = None,
) -> Any:
    """
    Получение списка покупок всех пользователей  со смещением и ограничением.
    """
    registry = await purchase_crud.get_multi(db, skip=skip, limit=limit)
    return registry


@router.get("/by/registry/{registry_id}", response_model=List[schemas.PurchaseWithProductData])
async def read_purchase_by_registry_id(
    db: SessionInstance,
    registry_id: UUID4,
) -> List[schemas.PurchaseWithProductData]:
    """
    Получение списка покупок по записи из реестра  c доп информацией о товаре и стоимости.
    """
    query = (
                select(
                    Purchases.id,
                    Products.name,
                    Purchases.count,
                    Products.selling_cost.label('goods_cost'),
                    (Purchases.count * Products.selling_cost).label('total_cost')
                    )
                .join(Products, Products.id == Purchases.product_id)
                .filter(Purchases.registry_id == registry_id)
            )
    result = await db.execute(query)

    return result.all()


@router.post("/", response_model=schemas.PurchaseItem)
async def create_purchase(
    *,
    db: SessionInstance,
    purchase_in: schemas.PurchaseCreate,
) -> Any:
    """
    Создание новой записи в реестре покупупок.
    """
    await check_by_id(db, purchase_registry_crud, id=purchase_in.registry_id,
                msg="Запись в реестре покупок с id = %s  не существует")
    await check_by_id(db, product_crud, id=purchase_in.product_id, msg="Продукт с id = %s  не существует")
    purchase = await purchase_crud.create(db, obj_in=purchase_in)

    return purchase


@router.get("/{purchase_id}", response_model=schemas.PurchaseItem)
async def read_purchase_by_id(
    purchase_id: UUID4,
    db: SessionInstance,
) -> Any:
    """
    Получение записи из реестра покупок по id.
    """
    purchase = await check_by_id(db, purchase_crud, id=purchase_id,
                                 msg="Покупка с id = %s  не существует")
    return purchase


@router.put("/{purchase_id}", response_model=schemas.PurchaseItem)
async def update_purchase(
    *,
    db: SessionInstance,
    purchase_id: UUID4,
    purchase_in: schemas.PurchaseUpdate,
) -> Any:
    """
    Обновление данных записи реестра покупок с переданным id.
    """
    purchase=await check_by_id(db, purchase_crud, id=purchase_id,
                msg="Покупка с id = %s  не существует")
    registry_id_val = purchase_in.dict().get('registry_id')
    if registry_id_val:
        await check_by_id(db, purchase_registry_crud, id=registry_id_val,
                            msg="Запись в реестре покупок с id = %s  не существует")
    product_id_val = purchase_in.dict().get('product_id')
    if product_id_val:
        await check_by_id(db, product_crud, id=product_id_val, msg="Продукт с id = %s  не существует")
    purchase = await purchase_crud.update(db, db_obj=purchase, obj_in=purchase_in)
    return purchase


@router.delete("/{purchase_id}")
async def delete_registry(db: SessionInstance, purchase_id: UUID4) -> schemas.Msg:
    """
    Удаление записи в реестре покупок по id.
    """
    purchase = await check_by_id(db, purchase_crud, id=purchase_id,
                msg="Покупка с id = %s  не найдена")

    await purchase_crud.delete(db, model_item=purchase)
    return schemas.Msg(msg=f"Покупка с id = {purchase_id} удалена")

