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
    purchase = await purchase_crud.get_multi(db, skip=skip, limit=limit)
    return purchase


@router.get("/by/registry/{registry_id}", response_model=List[schemas.PurchaseItem])
async def read_purchase_by_registry_id(
    db: SessionInstance,
    registry_id: UUID4,
) -> Any:
    """
    Получение списка покупок по записи из реестра  c доп информацией о товаре и стоимости.
    """
    await check_by_id(db, purchase_registry_crud, id=registry_id,
                      msg="Запись в реестре покупок с id = %s  не существует")
    purchase = await purchase_crud.get_multi_by_filter(db, filter_list=[(Purchases.registry_id == registry_id)])
    return purchase


@router.post("/", response_model=schemas.PurchaseItem)
async def create_purchase(
    *,
    db: SessionInstance,
    purchase_in: schemas.PurchaseBase,
) -> Any:
    """
    Создание новой записи в реестре покупупок.
    """
    await check_by_id(db, purchase_registry_crud, id=purchase_in.registry_id,
                msg="Запись в реестре покупок с id = %s  не существует")
    product = await check_by_id(db, product_crud, id=purchase_in.product_id, msg="Продукт с id = %s  не существует")
    create_purchase_item = schemas.PurchaseCreate(
                                                    **purchase_in.model_dump(),
                                                    **{
                                                        "product_name": product.name,
                                                        "selling_cost": product.selling_cost,
                                                    })
    purchase = await purchase_crud.create(db, obj_in=create_purchase_item)

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



@router.delete("/{purchase_id}")
async def delete_registry(db: SessionInstance, purchase_id: UUID4) -> schemas.Msg:
    """
    Удаление записи в реестре покупок по id.
    """
    purchase = await check_by_id(db, purchase_crud, id=purchase_id,
                msg="Покупка с id = %s  не найдена")

    await purchase_crud.delete(db, model_item=purchase)
    return schemas.Msg(msg=f"Покупка с id = {purchase_id} удалена")

