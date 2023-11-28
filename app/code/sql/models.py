import enum
import uuid
from datetime import datetime as dt
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String,DateTime, Enum , Numeric
from sqlalchemy.orm import relationship

from sqlalchemy.dialects import postgresql


from .database import Base



class Gender(enum.Enum):
    male = 'male'
    female = 'female'

class Users(Base):
    __tablename__ = "users"
    id = Column(postgresql.UUID(as_uuid = True), default=uuid.uuid4, primary_key=True)
    full_name = Column(String(50), nullable = False)
    birth_year = Column(Integer(), nullable = False)
    gender = Column(Enum(Gender,
                                values_callable = lambda x: [str(member.value) for member in Gender]),
                                default=Gender.male, nullable=False)
    processing_consent = Column(Boolean(), nullable=False)
    registration_date = Column(DateTime(timezone=True), default= dt.utcnow(), nullable=False)

    registry =relationship(
        'PurchaseRegistry',
        back_populates='user',
        cascade='save-update, merge, delete',
        passive_deletes=True,
    )


class Products(Base):
    __tablename__ = "products"
    id = Column(postgresql.UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    name = Column(String(50), nullable = False)
    purchase_cost = Column(Numeric(), nullable = False)
    selling_cost = Column(Numeric(), nullable = False)
    product_purchases = relationship('Purchases', backref='products', passive_deletes=True)


class PurchaseRegistry(Base):
    __tablename__ = "purchase_registry"
    id = Column(postgresql.UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    user_id = Column(postgresql.UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    purchase_date = Column(DateTime(timezone=True), default= dt.utcnow(), nullable=False)
    purchases = relationship(
        'Purchases',
        back_populates='registry',
        cascade='save-update, merge, delete',
        passive_deletes=True,
    )
    user = relationship(
        'Users',
        back_populates='registry',
    )


class Purchases(Base):
    __tablename__ = "purchases"
    id = Column(postgresql.UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    registry_id = Column(postgresql.UUID(as_uuid=True),  ForeignKey('purchase_registry.id', ondelete='CASCADE'), nullable=False)
    product_id = Column(postgresql.UUID(as_uuid=True), ForeignKey('products.id', ondelete='CASCADE'), nullable=False)
    count = Column(Integer(), nullable=False)

    registry = relationship(
        'PurchaseRegistry',
        back_populates='purchases',
    )

