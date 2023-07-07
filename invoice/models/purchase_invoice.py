from django.db import models
from authuser.models import User
from common.models import TimestampsFieldMixin

from companyinfo.models import BranchFieldMixin, CompanyInfo
from fiscalyear.models import FiscalYear, FiscalYearFieldMixin
from invoice.models.purchase_invoice_image import PurchaseInvoiceImage
from supplier.models import Supplier


class PurchaseInvoiceQuerySet(models.QuerySet):
    def get_invoice_of_branch(self, branch=None, fiscal_year=None):
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


class PurchaseInvoiceManager(models.Manager):
    def get_queryset(self):
        return PurchaseInvoiceQuerySet(self.model, using=self._db)

    def get_invoice_of_branch(self, branch=None, fiscal_year=None):
        return self.get_queryset().get_invoice_of_branch(branch, fiscal_year)


class PurchaseInvoice(
    BranchFieldMixin, FiscalYearFieldMixin, TimestampsFieldMixin, models.Model
):
    invoice_image = models.OneToOneField(
        PurchaseInvoiceImage,
        null=True,
        blank=True,
        on_delete=models.RESTRICT,
        related_name="purchase_invoice",
    )
    supplier = models.ForeignKey(Supplier, on_delete=models.RESTRICT)
    purchase_date = models.DateTimeField()
    ref_bill_no = models.CharField(max_length=50)
    gross_amount = models.DecimalField(max_digits=16, decimal_places=4, default=0.0)
    tax_vat_amount = models.DecimalField(max_digits=16, decimal_places=4, default=0.0)
    discount_amount = models.DecimalField(max_digits=16, decimal_places=4, default=0.0)
    net_amount = models.DecimalField(max_digits=16, decimal_places=4, default=0.0)
    created_by = models.ForeignKey(User, on_delete=models.RESTRICT)
    payment_mode = models.CharField(max_length=150)

    objects = PurchaseInvoiceManager()

    def __str__(self) -> str:
        return (
            f"{self.id}: {self.purchase_date.strftime('%Y-%d-%m')} {self.supplier.name}"
        )
