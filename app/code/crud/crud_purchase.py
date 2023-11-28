from .base import CRUDBase
from sql.models import Purchases
from schemas import PurchaseCreate


class CRUDPurchase(CRUDBase[Purchases, PurchaseCreate]):
    pass


purchase = CRUDPurchase(Purchases)
