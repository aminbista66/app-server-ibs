from django.db import models
from common.models import TimestampsFieldMixin

from companyinfo.models import BranchFieldMixin, CompanyInfo
from fiscalyear.models import FiscalYear, FiscalYearFieldMixin



class InventoryCategoryQuerySet(models.QuerySet):
    def get_category_of_branch(self, branch=None, fiscal_year=None):
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
    

class InventoryCategoryManager(models.Manager):
    def get_queryset(self):
        return InventoryCategoryQuerySet(self.model, using=self._db)
    
    def get_category_of_branch(self, branch=None, fiscal_year=None):
        return self.get_queryset().get_category_of_branch(branch, fiscal_year)
    

class InventoryCategory(BranchFieldMixin, FiscalYearFieldMixin, TimestampsFieldMixin, models.Model):
    class CategoryStatus(models.TextChoices):
        ACTIVE = "active", "Active"
        INACTIVE = "inactive", "Inactive"

    name = models.CharField(max_length=100)
    status = models.CharField(max_length=15, choices=CategoryStatus.choices, default=CategoryStatus.ACTIVE)
    description = models.CharField(max_length=300, null=True, blank=True)

    objects = InventoryCategoryManager()

    class Meta: 
        verbose_name_plural = "inventory categories"

    def __str__(self) -> str:
        return self.name