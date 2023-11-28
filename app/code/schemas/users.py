from typing import Optional, Union
from datetime import  datetime

from pydantic import BaseModel, Field, field_validator
from pydantic.types import UUID4

from sql.models import Gender


class UserBase(BaseModel):
    full_name: str = Field(..., max_length=50)
    gender: Gender
    birth_year: int = Field(..., gt=1900, lt=2023)
    processing_consent: bool

    @field_validator('processing_consent')
    @classmethod
    def MustBeTrue(cls, value):
        assert value == True, 'Подтвердите согласие на обработку ПД, чтобы продолжить'

        return value

class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    full_name:str = Field(None, max_length=50)
    gender: Union[Gender,None] = None
    birth_year:int =  Field(None, gt=1900, lt=2023)


class UserInDBBase(UserBase):
    id: Optional[UUID4] = None
    registration_date: datetime = datetime.utcnow()

    class Config:
        from_attributes = True


class User(UserInDBBase):
    pass

