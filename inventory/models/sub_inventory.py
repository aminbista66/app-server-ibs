from django.db import models
from common.models import TimestampsFieldMixin
from companyinfo.models import BranchFieldMixin
from inventory.models.inventory_item import InventoryItem
from inventory.models.sub_store import SubStore


class SubInventory(models.Model):
    sub_store = models.ForeignKey(SubStore, on_delete=models.RESTRICT)
    item = models.ForeignKey(InventoryItem, on_delete=models.RESTRICT)
    quantity = models.DecimalField(max_digits=12, decimal_places=4, default="0.0000")
    total_deduction = models.DecimalField(max_digits=12, decimal_places=4, default="0.0000")

    def __str__(self) -> str:
        return f"{self.item.name}:{self.sub_store.name}:{self.quantity}"
    
    class Meta:
        verbose_name = "sub-inventory"
        verbose_name_plural = "sub-inventories"
        unique_together = ["sub_store", "item"]