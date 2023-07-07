from django.db import models
from django.db.models.query import QuerySet
from common.utils import image_validate
from companyinfo.models import CompanyInfo, BranchFieldMixin
from .utils import get_upload_folder


class SupplierQuerySet(models.QuerySet):
    def get_supplier_of_branch(self, branch=None):
        _branch = (
            branch
            if branch is not None and branch != ""
            else CompanyInfo.objects.first()
        )
        return self.filter(branch=_branch) 

class SupplierManager(models.Manager):
    def get_queryset(self):
        return SupplierQuerySet(self.model, using=self._db)
    
    def get_supplier_of_branch(self, branch=None):
        return self.get_queryset().get_supplier_of_branch(branch)
        

class Supplier(BranchFieldMixin, models.Model):
    image = models.ImageField(upload_to=get_upload_folder, validators=[image_validate], null=True, blank=True)
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=100, unique= True)
    address = models.CharField(max_length=100)
    phone_number = models.PositiveBigIntegerField(unique=True, null=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    objects = SupplierManager()

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "suppliers"