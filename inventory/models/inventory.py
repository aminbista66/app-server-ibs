from django.db import models
from common.models import TimestampsFieldMixin

from companyinfo.models import BranchFieldMixin, CompanyInfo
from fiscalyear.models import FiscalYear, FiscalYearFieldMixin
from inventory.models.inventory_item import InventoryItem
from inventory.models.sub_inventory import SubInventory

class InventoryQuerySet(models.QuerySet):
    def get_inventory_of_branch(self, branch=None, fiscal_year=None):
        _branch = (
            branch
            if branch is not None and branch != ""
            else CompanyInfo.objects.first()
        )
        _fiscal_year = (
            fiscal_year
            if fiscal_year is not None and fiscal_year != ""
            else FiscalYear.objects.using("default").filter(is_active=True).first()
        )
        return self.filter(branch=_branch, fiscal_year=_fiscal_year)

class InventoryManager(models.Manager):
    def get_queryset(self):
        return InventoryQuerySet(self.model, using=self._db)
    
    def get_inventory_of_branch(self, branch=None, fiscal_year=None):
        return self.get_queryset().get_inventory_of_branch(branch, fiscal_year)
    

class Inventory(BranchFieldMixin, FiscalYearFieldMixin, TimestampsFieldMixin, models.Model):
    item = models.OneToOneField(InventoryItem, on_delete=models.RESTRICT)
    quantity = models.DecimalField(max_digits=12, decimal_places=4, default=0.0)
    sub_inventories = models.ManyToManyField(SubInventory,)
    purchased_stock = models.PositiveIntegerField(default=0)


    objects = InventoryManager()

    def __str__(self) -> str:
        return self.item.name
    
    class Meta:
        verbose_name_plural = "inventories"