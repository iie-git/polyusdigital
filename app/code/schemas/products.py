from typing import Optional, Union
from decimal import Decimal

from pydantic import BaseModel, Field
from pydantic.types import UUID4


class ProductBase(BaseModel):
    name: str = Field(..., max_length=50)
    purchase_cost: Decimal
    selling_cost: Decimal


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    name: str = Field(None, max_length=50)
    purchase_cost: Union[Decimal, None] = None
    selling_cost: Union[Decimal, None] = None


class ProductInDBBase(ProductBase):
    id: Optional[UUID4] = None

    class Config:
        from_attributes = True


class Product(ProductInDBBase):
    pass

