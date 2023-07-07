from django.db import models

from .utils import fiscal_year_generator, validate_fiscal_year


class FiscalYear(models.Model):
    fiscal_year = models.CharField(max_length=10, validators=[validate_fiscal_year], primary_key=True, editable=False)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.fiscal_year
    



class FiscalYearFieldMixin(models.Model):
    fiscal_year = models.CharField(max_length=10, validators=[validate_fiscal_year])

    class Meta:
        abstract = True