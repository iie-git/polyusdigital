from typing import Any, List, Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import UUID4

import schemas
from crud import purchase_registry as purchase_registry_crud
from crud import purchase as purchase_crud
from crud import user as user_crud
from crud import check_by_id
from api import deps

from sql.models import Purchases



router = APIRouter()
SessionInstance = Annotated[AsyncSession, Depends(deps.get_session)]


@router.get("/", response_model=List[schemas.PurchaseRegistryItem])
async def read_registry(
    db: SessionInstance,
    skip: int = None,
    limit: int = None,
) -> Any:
    """
    Получение списка всех записей в реестре покупок со смещением и ограничением.
    """
    registry = await purchase_registry_crud.get_multi(db, skip=skip, limit=limit)
    return registry


@router.post("/", response_model=schemas.PurchaseRegistryItem)
async def create_registry(
    *,
    db: SessionInstance,
    registry_in: schemas.PurchaseRegistryBase,
) -> Any:
    """
    Создание новой записи в реестре покупупок.
    """
    user_obj = await check_by_id(db, user_crud, id=registry_in.user_id, msg="Пользователь с id = %s  не существует")
    create_registry_item = schemas.PurchaseRegistryCreate(**registry_in.model_dump(), **{"user_full_name": user_obj.full_name})
    registry = await purchase_registry_crud.create(db, obj_in=create_registry_item)
    return registry


@router.get("/{registry_id}", response_model=schemas.PurchaseRegistryItem)
async def read_registry_by_id(
    registry_id: UUID4,
    db: SessionInstance,
) -> Any:
    """
    Получение записи из реестра покупок по id.
    """
    registry = await check_by_id(
                                db,
                                purchase_registry_crud,
                                id=registry_id,
                                msg="Запись в реестре покупок с id = %s  не существует"
                                )
    return registry


@router.delete("/{registry_id}")
async def delete_registry(db: SessionInstance, registry_id: UUID4) -> schemas.Msg:
    """
    Удаление записи в реестре покупок по id.
    """
    registry = await check_by_id(db, purchase_registry_crud, id=registry_id,
                                 msg="Запись в реестре покупок с id = %s не найдена")
    purchase_with_registry = await purchase_crud.get_multi_by_filter(
                                                            db,
                                                            filter_list=[(Purchases.registry_id == registry_id)],
                                                            limit=1)
    if purchase_with_registry:
        raise HTTPException(
            status_code=409,
            detail=f"Невозмождно удалить запись реестра {registry_id}, у которой имеется в покупка"
        )
    await purchase_registry_crud.delete(db, model_item=registry)
    return schemas.Msg(msg=f"Запись в реестре покупок с id = {registry_id} удалена")

