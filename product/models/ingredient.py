from django.db import models
from common.models import TimestampsFieldMixin

from companyinfo.models import BranchFieldMixin, CompanyInfo
from fiscalyear.models import FiscalYear, FiscalYearFieldMixin
from inventory.models.inventory_item import InventoryItem
from inventory.models.sub_store import SubStore
from product.models.product import Product

class ProductIngredientQuerySet(models.QuerySet):
    def get_ingredient_of_branch(self, branch=None, fiscal_year=None):
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


class ProductIngredientManager(models.Manager):
    def get_queryset(self):
        return ProductIngredientQuerySet(self.model, using=self._db)

    def get_ingredient_of_branch(self, branch=None, fiscal_year=None):
        return self.get_queryset().get_ingredient_of_branch(branch, fiscal_year)
    

class ProductIngredient(BranchFieldMixin, FiscalYearFieldMixin, TimestampsFieldMixin, models.Model):
    item = models.ForeignKey(InventoryItem, on_delete=models.RESTRICT, related_name="product_ingredients")
    store = models.ForeignKey(SubStore, on_delete=models.RESTRICT)
    quantity = models.DecimalField(max_digits=12, decimal_places=4, default=0.0)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_ingredients")

    objects = ProductIngredientManager()

    class Meta:
        verbose_name = "product ingredient"
        verbose_name_plural = "product ingredients"

    def __str__(self):
        return f"{self.product.name} | {self.item.name}"
