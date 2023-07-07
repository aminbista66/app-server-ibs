from django.db import models

from companyinfo.models import BranchFieldMixin, CompanyInfo
from fiscalyear.models import FiscalYear, FiscalYearFieldMixin


# Tax Rule


class TaxRuleQuerySet(models.QuerySet):
    def get_tax_rule_of_branch(self, branch=None, fiscal_year=None):
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


class TaxRuleManager(models.Manager):
    def get_queryset(self):
        return TaxRuleQuerySet(self.model, using=self._db)

    def get_tax_rule_of_branch(self, branch=None, fiscal_year=None):
        return self.get_queryset().get_tax_rule_of_branch(branch, fiscal_year)


class TaxRule(BranchFieldMixin, FiscalYearFieldMixin, models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        INACTIVE = "inactive", "Inactive"

    name = models.CharField(max_length=150)
    rate = models.DecimalField(max_digits=10, decimal_places=2, help_text="Tax rate should be in percentage")
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.ACTIVE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = TaxRuleManager()

    class Meta:
        verbose_name = "tax rule"

    def __str__(self) -> str:
        return self.name


# End Tax Rule


# Discount Rule


class DiscountRuleQuerySet(models.QuerySet):
    def get_discount_rule_of_branch(self, branch=None, fiscal_year=None):
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
        return self.filter(branch=_branch)


class DiscountRuleManager(models.Manager):
    def get_queryset(self):
        return DiscountRuleQuerySet(self.model, using=self._db)

    def get_discount_rule_of_branch(self, branch=None, fiscal_year=None):
        return self.get_queryset().get_discount_rule_of_branch(branch, fiscal_year)


class DiscountRule(BranchFieldMixin, FiscalYearFieldMixin, models.Model):
    
    class DiscountType(models.TextChoices):
        FIXED = "fixed", "Fixed",
        PERCENTAGE = "percentage", "Percentage"
    
    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        INACTIVE = "inactive", "Inactive"

    name = models.CharField(max_length=150)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=15, choices=DiscountType.choices)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.ACTIVE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = DiscountRuleManager()

    class Meta:
        verbose_name = "discount rule"

    def __str__(self) -> str:
        return self.name
# End Discount Rule

