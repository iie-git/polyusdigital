from typing import Optional, Union
from decimal import Decimal

from pydantic import BaseModel, Field
from pydantic.types import UUID4


class ProductBase(BaseModel):
    purchase_cost: Decimal = Field(..., gt=0)
    selling_cost: Decimal = Field(..., gt=0)

class ProductWithFloatCost(BaseModel):

    purchase_cost: float = Field(..., gt=0)
    selling_cost: float = Field(..., gt=0)

class ProductNoneUpdate(BaseModel):
    name: str = Field(..., max_length=50)


class ProductCreate(ProductBase, ProductNoneUpdate):
    pass


class ProductUpdate(ProductBase):
    purchase_cost: Decimal = Field(None, gt=0)
    selling_cost: Decimal = Field(None, gt=0)



class ProductInDBBase(ProductWithFloatCost,ProductNoneUpdate):
    id: Optional[UUID4] = None

    class Config:
        from_attributes = True


class Product(ProductInDBBase):
    pass

