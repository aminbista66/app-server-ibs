from django.db import models

from common.utils import image_validate
from companyinfo.utils import get_upload_folder
from fiscalyear.models import FiscalYearFieldMixin

class CompanyInfo(FiscalYearFieldMixin, models.Model):
    class COMPANY_PANVAT_TYPE(models.TextChoices):
        PAN = "PAN", "PAN"
        VAT = "VAT", "VAT"

    class CURRENCY(models.TextChoices):
        NPR = "NPR", "NPR"
        INR = "INR", "INR"
        USD = "USD", "USD"

    class STATUS_TYPE(models.TextChoices):
        ACTIVE = "active", "Active"
        INACTIVE = "inactive", "Inactive"

    """
    A single company can register multiple branches 
    """
    logo = models.ImageField(upload_to=get_upload_folder, validators=[image_validate], null=True, blank=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    pan_no = models.CharField(max_length=20, unique=True, db_index=True)
    message = models.TextField(null=True, blank=True)
    tax = models.DecimalField(default=0.0, decimal_places=5, max_digits=30, help_text="Specify in %")
    service_charge = models.DecimalField(default=0.0, decimal_places=5, max_digits=30)
    currency = models.CharField(max_length=10, choices=CURRENCY.choices, default=CURRENCY.NPR)
    is_company_vat_pan = models.CharField(max_length=5, choices=COMPANY_PANVAT_TYPE.choices, default=COMPANY_PANVAT_TYPE.PAN)
    cmbs_username = models.CharField(max_length=50)
    cmbs_password = models.CharField(max_length=50)
    message = models.CharField(max_length=100)
    status = models.CharField(max_length=10, choices=STATUS_TYPE.choices, default=STATUS_TYPE.ACTIVE)
    facebook_link = models.CharField(max_length=100, null=True)
    instagram_link = models.CharField(max_length=100, null=True)
    twitter_link = models.CharField(max_length=100, null=True)
    linkedin_link = models.CharField(max_length=100, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    # objects = CompanyInfoManager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "company info"



class BranchFieldMixin(models.Model):
    branch = models.ForeignKey(CompanyInfo, on_delete=models.RESTRICT)

    class Meta:
        abstract = True