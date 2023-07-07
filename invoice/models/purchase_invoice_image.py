from django.db import models
from common.utils import image_validate
from companyinfo.models import BranchFieldMixin, CompanyInfo

from invoice.utils import get_purchase_invoice_image_upload_folder


class PurchaseInvoiceImageQuerySet(models.QuerySet):
    def get_image_of_branch(self, branch=None):
        _branch = (
            branch
            if branch is not None and branch != ""
            else CompanyInfo.objects.first()
        )
        return self.filter(branch=_branch)

class PurchaseInvoiceImageManager(models.Manager):
    def get_queryset(self):
        return PurchaseInvoiceImageQuerySet(self.model, using=self._db)
    
    def get_image_of_branch(self, branch=None):
        return self.get_queryset().get_image_of_branch(branch)



class PurchaseInvoiceImage(BranchFieldMixin, models.Model):
    image = models.ImageField(upload_to=get_purchase_invoice_image_upload_folder, validators=[image_validate])

    objects = PurchaseInvoiceImageManager()
    
    def __str__(self):
        return self.image.name
    class Meta:
        verbose_name = "Purchase Invoice Image"
        verbose_name_plural = "Purchase Invoicee Images"