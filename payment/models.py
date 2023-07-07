from django.db import models
from common.utils import image_validate

from companyinfo.models import BranchFieldMixin, CompanyInfo

from .utils import get_upload_folder

class PaymentMethodQuerySet(models.QuerySet):
    def get_payment_method_of_branch(self, branch=None):
        _branch = branch if branch is not None and branch != "" else CompanyInfo.objects.first()
        return self.filter(branch=_branch)

class PaymentMethodManager(models.Manager):
    def get_queryset(self):
        return PaymentMethodQuerySet(self.model, using=self._db)
    
    def get_payment_method_of_branch(self, branch=None):
        return self.get_queryset().get_payment_method_of_branch(branch)

# Create your models here.
class PaymentMethod(BranchFieldMixin, models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        INACTIVE = "inactive", "Inactive"

    image = models.ImageField(upload_to=get_upload_folder, validators=[image_validate], null=True, blank=True)
    method = models.CharField(max_length=150)
    code = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = PaymentMethodManager()

    class Meta:
        verbose_name = "payment method"