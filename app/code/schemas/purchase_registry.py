from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field
from pydantic.types import UUID4


class PurchaseRegistryBase(BaseModel):
    user_id: UUID4
    purchase_date: datetime = datetime.utcnow()


class PurchaseRegistryCreate(PurchaseRegistryBase):
    user_full_name: str = Field(..., max_length=50)




class PurchaseRegistryInDBBase(PurchaseRegistryBase):
    id: Optional[UUID4] = None
    user_full_name: str = Field(..., max_length=50)

    class Config:
        from_attributes = True


class PurchaseRegistryItem(PurchaseRegistryInDBBase):
    pass

