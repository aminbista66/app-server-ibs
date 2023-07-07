from django.db import models
from common.models import TimestampsFieldMixin

from companyinfo.models import BranchFieldMixin, CompanyInfo


class SubStoreQuerySet(models.QuerySet):
    def get_substore_of_branch(self, branch=None):
        _branch = (
            branch
            if branch is not None and branch != ""
            else CompanyInfo.objects.first()
        )
        return self.filter(branch=_branch)

class SubStoreManager(models.Manager):
    def get_queryset(self):
        return SubStoreQuerySet(self.model, using=self._db)
    
    def get_substore_of_branch(self, branch=None):
        return self.get_queryset().get_substore_of_branch(branch)


class SubStore(BranchFieldMixin, TimestampsFieldMixin, models.Model):
    name = models.CharField(max_length=100, unique=True)

    objects = SubStoreManager()

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name = "sub-store"
        verbose_name_plural= "sub-stores"