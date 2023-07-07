from django.db import models
from common.models import TimestampsFieldMixin
from common.utils import image_validate

from companyinfo.models import BranchFieldMixin, CompanyInfo
from product.utils import get_product_image_upload_folder


class ProductImageQuerySet(models.QuerySet):
    def get_image_of_branch(self, branch=None):
        _branch = (
            branch
            if branch is not None or branch != ""
            else CompanyInfo.objects.first()
        )
        return self.filter(branch=_branch)


class ProductImageManager(models.Manager):
    def get_queryset(self):
        return ProductImageQuerySet(self.model, using=self._db)
    
    def get_image_of_branch(self, branch=None):
        return self.get_queryset().get_image_of_branch(branch)
    

class ProductImage(BranchFieldMixin, models.Model):
    image = models.ImageField(upload_to=get_product_image_upload_folder, validators=[image_validate])

    objects = ProductImageManager()

    def __str__(self) -> str:
        return self.image.name