from typing import Any, List, Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import UUID4

import schemas
from crud import purchase_registry as purchase_registry_crud
from crud import user as user_crud
from api import deps

from crud import check_by_id


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
    registry_in: schemas.PurchaseRegistryCreate,
) -> Any:
    """
    Создание новой записи в реестре покупупок.
    """
    await check_by_id(db, user_crud, id=registry_in.user_id, msg="Пользователь с id = %s  не существует")

    registry = await purchase_registry_crud.create(db, obj_in=registry_in)
    return registry


@router.get("/{registry_id}", response_model=schemas.PurchaseRegistryItem)
async def read_registry_by_id(
    registry_id: UUID4,
    db: SessionInstance,
) -> Any:
    """
    Получение записи из реестра покупок по id.
    """
    registry = await check_by_id(db, purchase_registry_crud, id=registry_id,
                                     msg="Запись в реестре покупок с id = %s  не существует")
    return registry


@router.put("/{registry_id}", response_model=schemas.PurchaseRegistryItem)
async def update_registry(
    *,
    db: SessionInstance,
    registry_id: UUID4,
    registry_in: schemas.PurchaseRegistryUpdate,
) -> Any:
    """
    Обновление данных записи реестра покупок с переданным id.
    """
    registry = await check_by_id(db, purchase_registry_crud, id=registry_id,
                                    msg="Запись в реестре покупок с id = %s не существует")

    user_id_val = registry_in.dict().get('user_id')
    if user_id_val:
        await check_by_id(db, user_crud, id=registry_in.user_id, msg="Пользователь с id = %s  не существует")
    registry = await purchase_registry_crud.update(db, db_obj=registry, obj_in=registry_in)
    return registry



@router.delete("/{registry_id}")
async def delete_registry(db: SessionInstance, registry_id: UUID4) -> schemas.Msg:
    """
    Удаление записи в реестре покупок по id.
    """
    registry = await check_by_id(db, purchase_registry_crud, id=registry_id,
                                 msg="Запись в реестре покупок с id = %s не найдена")

    await purchase_registry_crud.delete(db, model_item=registry)
    return schemas.Msg(msg=f"Запись в реестре покупок с id = {registry_id} удалена")

