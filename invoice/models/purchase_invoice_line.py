from django.db import models
from common.models import TimestampsFieldMixin

from companyinfo.models import BranchFieldMixin, CompanyInfo
from fiscalyear.models import FiscalYear, FiscalYearFieldMixin
from inventory.models.inventory_item import InventoryItem
from invoice.models.purchase_invoice import PurchaseInvoice


class PurchaseInvoiceLineQuerySet(models.QuerySet):
    def get_inventory_purchase_history_of_branch(self, branch=None, fiscal_year=None):
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


class PurchaseInvoiceLineManager(models.Manager):
    def get_queryset(self):
        return PurchaseInvoiceLineQuerySet(self.model, using=self._db)

    def get_inventory_purchase_history_of_branch(self, branch=None, fiscal_year=None):
        return self.get_queryset().get_inventory_purchase_history_of_branch(
            branch, fiscal_year
        )


class PurchaseInvoiceLine(
    BranchFieldMixin, FiscalYearFieldMixin, TimestampsFieldMixin, models.Model
):
    invoice = models.ForeignKey(PurchaseInvoice, on_delete=models.CASCADE, related_name="purchase_invoice_lines")
    inventory_item = models.ForeignKey(InventoryItem, on_delete=models.RESTRICT)
    quantity = models.DecimalField(max_digits=12, decimal_places=4, default=0.0)
    total = models.DecimalField(max_digits=16, decimal_places=4)

    objects = PurchaseInvoiceLineManager()

    def __str__(self) -> str:
        return f"{str(self.invoice.id)}: {self.inventory_item.name} - {str(self.quantity)}"

