from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic.types import UUID4


class PurchaseRegistryBase(BaseModel):
    user_id: UUID4
    purchase_date: datetime = datetime.utcnow()


class PurchaseRegistryCreate(PurchaseRegistryBase):
    pass


class PurchaseRegistryUpdate(PurchaseRegistryBase):
    user_id: Optional[UUID4] = None
    purchase_date: datetime = datetime.utcnow()


class PurchaseRegistryInDBBase(PurchaseRegistryBase):
    id: Optional[UUID4] = None
    purchase_date: Optional[datetime] = None

    class Config:
        from_attributes = True


class PurchaseRegistryItem(PurchaseRegistryInDBBase):
    pass

