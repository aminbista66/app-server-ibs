from django.db import models
from common.utils import image_validate
from companyinfo.models import CompanyInfo, BranchFieldMixin
from .utils import get_upload_folder

class CustomerQuerySet(models.QuerySet):
    def get_customer_of_branch(self, branch=None):
        _branch = (
            branch
            if branch is not None and branch != ""
            else CompanyInfo.objects.first()
        )
        return self.filter(branch=_branch)


class CustomerManager(models.Manager):
    def get_queryset(self):
        return CustomerQuerySet(self.model, using=self._db)

    def get_customer_of_branch(self, branch=None):
        return self.get_queryset().get_customer_of_branch(branch)


class Customer(BranchFieldMixin, models.Model):
    class ID(models.TextChoices):
        LICENSE = 'license', 'License'
        PASSPORT = 'passport', 'Passport'
        CITIZENSHIP = 'citizenship', 'Citizenship'
        NID = 'national_id', 'National ID'

    image1 = models.ImageField(upload_to=get_upload_folder, validators=[image_validate], null=True, blank=True)
    image2 = models.ImageField(upload_to=get_upload_folder, validators=[image_validate], null=True, blank=True)
    id_type = models.CharField(max_length=48, null=True, blank=True, choices=ID.choices)
    name = models.CharField(
        max_length=150,
    )
    email = models.EmailField(max_length=150, null=True, blank=True)
    phone1 = models.CharField(max_length=15, unique=True)
    phone2 = models.CharField(max_length=15, null=True, blank=True)
    points_earned = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomerManager()

    def __str__(self):
        return self.name

'''
class CustomerDocumentImage(models.Model):
    image = models.ImageField(upload_to=get_upload_folder, validators=[image_validate], null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    type = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self) -> str:
        return f'{self.type} | {self.customer.name} | {self.customer.branch.name}'
'''