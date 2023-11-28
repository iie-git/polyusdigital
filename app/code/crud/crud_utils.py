from typing import Any, Union
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from .base import CRUDBase


async def check_by_id(db: AsyncSession, crud: CRUDBase, *, id: Any = None, msg: str = '') -> Union[HTTPException, Any]:
    '''Проверка наличия объекта по id  c использованием crud, если он есть, то возвращет его,ошибка в обратном случае'''
    result = await crud.get(db, id=id)
    if not result:
        raise HTTPException(
            status_code=404,
            detail=msg % id
        )
    return result


