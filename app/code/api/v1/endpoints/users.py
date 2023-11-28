from typing import Any, List, Annotated

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import UUID4

import schemas
from crud import user as user_crud
from crud import check_by_id
from api import deps


router = APIRouter()
SessionInstance = Annotated[AsyncSession, Depends(deps.get_session)]


@router.get("/", response_model=List[schemas.User])
async def read_users(
    db: SessionInstance,
    skip: int = None,
    limit: int = None,
) -> Any:
    """
    Получение списка всех пользователей со смещением и ограничением.
    """
    users = await user_crud.get_multi(db, skip=skip, limit=limit)
    return users


@router.post("/", response_model=schemas.User)
async def create_user(
    *,
    db: SessionInstance,
    user_in: schemas.UserCreate,

) -> Any:
    """
    Создание нового пользователя.
    """
    user = await user_crud.create(db, obj_in=user_in)
    return user


@router.get("/{user_id}", response_model=schemas.User)
async def read_user_by_id(
    user_id: UUID4,
    db: SessionInstance,
) -> Any:
    """
    Получение пользователя по id.
    """
    user = await user_crud.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail=f"Пользователь с id = {user_id}  не существует",
        )
    return user


@router.put("/{user_id}", response_model=schemas.User)
async def update_user(
    *,
    db: SessionInstance,
    user_id: UUID4,
    user_in: schemas.UserUpdate,
) -> Any:
    """
    Обновление данных пользователя с переданным id.
    """
    user = await check_by_id(db, user_crud, id=user_id, msg="Пользователь с id = %s  не существует")

    user = await user_crud.update(db, db_obj=user, obj_in=user_in)
    return user


@router.delete("/{user_id}")
async def delete_user(db: SessionInstance, user_id: UUID4) -> schemas.Msg:
    """
    Удаление пользователя по id.
    """
    user = await check_by_id(db, user_crud, id=user_id, msg="Пользователь с id = %s  не существует")

    await user_crud.delete(db, model_item=user)

    return schemas.Msg(msg=f"Пользователь с id = {user_id} удален")

