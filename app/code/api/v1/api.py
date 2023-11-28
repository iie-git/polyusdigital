from fastapi import APIRouter

from .endpoints import users
from .endpoints import products
from .endpoints import purchase_registry
from .endpoints import purchase
from .endpoints import reports

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(products.router, prefix="/products", tags=["products"])
api_router.include_router(purchase_registry.router, prefix="/registry", tags=["registry"])
api_router.include_router(purchase.router, prefix="/purchase", tags=["purchase"])
api_router.include_router(reports.router, prefix="/reports", tags=["reports"])