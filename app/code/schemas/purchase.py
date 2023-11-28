
from typing import Optional
from decimal import Decimal

from pydantic import BaseModel, Field
from pydantic.types import UUID4


class PurchaseBase(BaseModel):
    registry_id: UUID4
    product_id: UUID4
    count: int = Field(..., gt=0)

class PurchaseWithProductData(BaseModel):
    id: UUID4
    name: str
    count: int
    goods_cost: Decimal
    total_cost: Decimal

class PurchaseCreate(PurchaseBase):
    pass


class PurchaseUpdate(PurchaseBase):
    registry_id: Optional[UUID4] = None
    product_id: Optional[UUID4] = None
    count: int = Field(None, gt=0)


class PurchaseInDBBase(PurchaseBase):
    id: Optional[UUID4] = None

    class Config:
        from_attributes = True


class PurchaseItem(PurchaseInDBBase):
    pass

