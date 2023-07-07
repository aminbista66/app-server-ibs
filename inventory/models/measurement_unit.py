from django.db import models
from common.models import TimestampsFieldMixin

from companyinfo.models import BranchFieldMixin, CompanyInfo
from fiscalyear.models import FiscalYear, FiscalYearFieldMixin


class MeasurementUnitQuerySet(models.QuerySet):
    def get_measurement_unit_of_branch(self, branch=None, fiscal_year=None):
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

class MeasurementUnitManager(models.Manager):
    def get_queryset(self):
        return MeasurementUnitQuerySet(self.model, using=self._db)
    
    def get_measurement_unit_of_branch(self, branch=None, fiscal_year=None):
        return self.get_queryset().get_measurement_unit_of_branch(branch, fiscal_year)

class MeasurementUnit(BranchFieldMixin, FiscalYearFieldMixin, TimestampsFieldMixin, models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        INACTIVE = "inactive", "Inactive"

    name = models.CharField(max_length=100)
    code = models.CharField(max_length=15)
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.ACTIVE)
    
    objects = MeasurementUnitManager()

    def __str__(self) -> str:
        return self.name