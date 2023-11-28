
from typing import Optional
from decimal import Decimal

from pydantic import BaseModel, Field, computed_field
from pydantic.types import UUID4


class PurchaseBase(BaseModel):
    registry_id: UUID4
    product_id: UUID4
    count: int = Field(..., gt=0)


class PurchaseCreate(PurchaseBase):
    selling_cost: Decimal
    product_name: str = Field(..., max_length=50)

    @computed_field
    @property
    def total_cost(self) -> Decimal:
        return self.selling_cost * self.count


class PurchaseInDBBase(PurchaseBase):
    id: Optional[UUID4] = None
    selling_cost: float
    product_name: str = Field(..., max_length=50)
    total_cost: float


    class Config:
        from_attributes = True


class PurchaseItem(PurchaseInDBBase):
    pass

