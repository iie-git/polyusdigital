
from .base import CRUDBase, CRUDDelete
from sql.models import PurchaseRegistry
from schemas import PurchaseRegistryCreate


class CRUDPurchaseRegistry(CRUDBase[PurchaseRegistry, PurchaseRegistryCreate],CRUDDelete):
    pass


purchase_registry = CRUDPurchaseRegistry(PurchaseRegistry)
