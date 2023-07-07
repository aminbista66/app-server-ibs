from django.db import models
from django.db.models.query import QuerySet
from common.models import TimestampsFieldMixin

from companyinfo.models import BranchFieldMixin, CompanyInfo
from fiscalyear.models import FiscalYear, FiscalYearFieldMixin
from inventory.models.measurement_unit import MeasurementUnit
from product.models.product_category import ProductCategory
from product.models.product_image import ProductImage
from inventory.models.sub_store import SubStore
from accounting.models import DiscountRule, TaxRule


class ProductQuerySet(models.QuerySet):
    def get_product_of_branch(self, branch=None, fiscal_year=None):
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


class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def get_product_of_branch(self, branch=None, fiscal_year=None):
        return self.get_queryset().get_product_of_branch(branch, fiscal_year)


class Product(
    BranchFieldMixin, FiscalYearFieldMixin, TimestampsFieldMixin, models.Model
):
    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        INACTIVE = "inactive", "Inactive"

    class TaxChoice(models.TextChoices):
        TAXABLE = "taxable", "Taxable"
        NON_TAXABLE = "non_taxable", "Non Taxable"

    product_image = models.OneToOneField(
        ProductImage,
        null=True,
        blank=True,
        on_delete=models.RESTRICT,
        related_name="product",
    )
    name = models.CharField(max_length=200)
    category = models.ForeignKey(
        ProductCategory, on_delete=models.RESTRICT, related_name="products"
    )
    price = models.DecimalField(max_digits=12, decimal_places=4, default=0.0)
    unit = models.ForeignKey(MeasurementUnit, on_delete=models.RESTRICT)
    status = models.CharField(
        max_length=15, choices=Status.choices, default=Status.ACTIVE
    )
    tax_status = models.CharField(max_length=24, choices=TaxChoice.choices, default=TaxChoice.TAXABLE)
    tax_rule = models.ForeignKey(TaxRule, null=True, blank=True, on_delete=models.RESTRICT, related_name="product_tax_rule")
    discount_rule = models.ForeignKey(DiscountRule, null=True, blank=True, on_delete=models.RESTRICT, related_name="product_discount_rule")
    points = models.DecimalField(max_digits=12, default=0.0, null=True, blank=True, decimal_places=2)

    objects = ProductManager()

    def __str__(self) -> str:
        return self.name

    def net_price(self):
        net_price: float = self.price

        if self.discount_rule.status == 'active':
            discount_amount = self.discount_rule.amount
            if self.discount_rule.type == 'percentage':
                discount_amount = net_price * (self.discount_rule.amount / 100)
            net_price = net_price - discount_amount

        if self.tax_status == "taxable":
            if self.tax_rule.status == 'active':
                net_price = net_price + net_price * (self.tax_rule.rate / 100)

        return net_price
