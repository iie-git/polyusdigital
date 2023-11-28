from typing import Any, List, Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from pydantic import UUID4
import crud
import schemas
from api import deps

from sql.models import Purchases

router = APIRouter()

SessionInstance = Annotated[AsyncSession, Depends(deps.get_session)]


@router.get("/", response_model=List[schemas.Product])
async def read_products(
    db: SessionInstance,
    skip: int = None,
    limit: int = None,
) -> Any:
    """
    Получение списка всех продуктов со смещением и ограничением.
    """
    products = await crud.product.get_multi(db, skip=skip, limit=limit)
    return products


@router.post("/", response_model=schemas.Product)
async def create_product(
    *,
    db: SessionInstance,
    product_in: schemas.ProductCreate,
) -> Any:
    """
    Создание нового продукта.
    """

    product = await crud.product.create(db, obj_in=product_in)
    return product



@router.get("/{product_id}", response_model=schemas.Product)
async def read_product_by_id(
    product_id: UUID4,
    db: SessionInstance,
) -> Any:
    """
    Получение продукта по id.
    """
    product = await crud.check_by_id(db, crud.product, id=product_id,
                                 msg="Продукт с id = %s  не существует")
    return product


@router.put("/{product_id}", response_model=schemas.Product)
async def update_product(
    *,
    db: SessionInstance,
    product_id: UUID4,
    product_in: schemas.ProductUpdate,
) -> Any:
    """
    Обновление данных о продукте с переданным id.
    """
    product = await crud.check_by_id(db, crud.product, id=product_id,
                                     msg="Продукт с id = %s  не существует")
    product = await crud.product.update(db, db_obj=product, obj_in=product_in)
    return product


@router.delete("/{product_id}")
async def delete_product(db: SessionInstance, product_id: UUID4) -> schemas.Msg:
    """
    Удаление продукта по id.
    """
    product = await crud.check_by_id(db, crud.product, id=product_id,
                                     msg="Продукт с id = %s  не существует")
    purchase_with_product = await crud.purchase.get_multi_by_filter(db,
                                                                 filter_list=[(Purchases.product_id == product_id)],
                                                                 limit=1)
    if purchase_with_product:
        raise HTTPException(
            status_code=409,
            detail=f"Невозмождно удалить продукт {product_id}, который имеется в покупках"
        )
    await crud.product.delete(db, model_item=product)
    return schemas.Msg(msg=f"Продукт с id = {product_id} удален")
