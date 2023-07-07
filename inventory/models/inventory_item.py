from django.db import models

from common.models import TimestampsFieldMixin
from common.utils import image_validate
from companyinfo.models import BranchFieldMixin, CompanyInfo
from fiscalyear.models import FiscalYear, FiscalYearFieldMixin

from inventory.models.inventory_category import InventoryCategory
from inventory.models.measurement_unit import MeasurementUnit

from inventory.utils import get_upload_folder


class InventoryItemQuerySet(models.QuerySet):
    def get_item_of_branch(self, branch=None, fiscal_year=None):
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


class InventoryItemManager(models.Manager):
    def get_queryset(self):
        return InventoryItemQuerySet(self.model, using=self._db)

    def get_item_of_branch(self, branch=None, fiscal_year=None):
        return self.get_queryset().get_item_of_branch(branch, fiscal_year)


class InventoryItem(
    BranchFieldMixin, FiscalYearFieldMixin, TimestampsFieldMixin, models.Model
):
    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        INACTIVE = "inactive", "Inactive"

    image = models.ImageField(
        upload_to=get_upload_folder, validators=[image_validate], null=True, blank=True
    )
    name = models.CharField(max_length=150)
    category = models.ForeignKey(InventoryCategory, on_delete=models.RESTRICT)
    reorder_threshold = models.PositiveIntegerField()
    measurement_unit = models.ForeignKey(MeasurementUnit, on_delete=models.RESTRICT)
    unit_price = models.DecimalField(max_digits=12, decimal_places=4, default="0.0000")
    product_code = models.CharField(max_length=100)
    status = models.CharField(
        max_length=15, choices=Status.choices, default=Status.ACTIVE
    )

    objects = InventoryItemManager()

    def __str__(self) -> str:
        return self.name
