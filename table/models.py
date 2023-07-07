from django.db import models

from companyinfo.models import CompanyInfo, BranchFieldMixin


class TableCategoryQuerySet(models.QuerySet):
    def get_table_category_of_branch(self, branch=None):
        _branch = (
            branch
            if branch is not None and branch != ""
            else CompanyInfo.objects.first()
        )
        return self.filter(branch=_branch)


class TableCategoryManager(models.Manager):
    def get_queryset(self):
        return TableCategoryQuerySet(self.model, using=self._db)

    def get_table_category_of_branch(self, branch=None):
        return self.get_queryset().get_table_category_of_branch(branch)


class TableCategory(BranchFieldMixin, models.Model):
    class CategoryStatus(models.TextChoices):
        ACTIVE = "active", "Active"
        INACTIVE = "inactive", "Inactive"

    name = models.CharField(max_length=150, unique=True)
    category_status = models.CharField(
        max_length=15, choices=CategoryStatus.choices, default=CategoryStatus.ACTIVE
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = TableCategoryManager()

    class Meta:
        verbose_name_plural = "table categories"

    def __str__(self) -> str:
        return self.name


class TableQuerySet(models.QuerySet):
    def get_table_of_branch(self, branch=None):
        _branch = (
            branch
            if branch is not None and branch != ""
            else CompanyInfo.objects.first()
        )
        return self.filter(branch=_branch)


class TableManager(models.Manager):
    def get_queryset(self):
        return TableQuerySet(self.model, using=self._db)
    
    def get_table_of_branch(self, branch=None):
        return self.get_queryset().get_table_of_branch(branch)
    

class Table(BranchFieldMixin, models.Model):
    class TableStatus(models.TextChoices):
        FREE = "free", "Free"
        OCCUPIED = "occupied", "Occupied"
        RESERVED = "reserved", "Reserved"

    name = models.CharField(max_length=150, unique=True)
    table_category = models.ForeignKey(TableCategory, on_delete=models.RESTRICT)
    table_status = models.CharField(
        max_length=15, choices=TableStatus.choices, default=TableStatus.FREE
    )
    no_of_seat = models.PositiveIntegerField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = TableManager()

    def __str__(self) -> str:
        return self.name
