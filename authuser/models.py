from django.db import models
from django.db.models.query import QuerySet
from django.utils import timezone

# Create your models here.
from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import (
   AbstractUser
)
from companyinfo.models import CompanyInfo
from common.utils import image_validate

from .utils import get_upload_folder

class UserQuerySet(models.QuerySet):
    def get_user_of_self_branch(self, user=None):
        if user is not None:
            if user.is_tenantadmin:
                return self.all()
            else:
                if hasattr(user, "branch") and user.branch != None:
                    return self.filter(branch = user.branch)
                else:
                    return self.none()
        else:
            self.none()


class UserManager(BaseUserManager):
    def create_user(self, username, password, **extra_fields):
        """
        Creates and saves a User with the given username.
        """
        if not username:
            raise ValueError('Users must have an username')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    # def set_password(self, user, password):
    #     return user.set_password(password)
    
    def create_superuser(self, username, password, **extra_fields):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("superuser must have is_staff=True.")
        if extra_fields.get("is_superuser")is not True:
            raise ValueError("superuser must have is_superuser=True")
        
        return self.create_user(username, password, **extra_fields)
        
    def get_queryset(self):
        return UserQuerySet(self.model, using=self._db)
    
    def get_user_of_self_branch(self, user=None):
        return self.get_queryset().get_user_of_self_branch(user)
    

class User(AbstractUser):
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    image = models.ImageField(upload_to=get_upload_folder, validators=[image_validate], null=True, blank=True)
    first_name = models.CharField(max_length=200) 
    last_name = models.CharField(max_length=200)
    username = models.CharField(max_length=200, unique= True)
    email_confirmed = models.BooleanField(_("Invitation and email confirmation status"), default=False)
    email_confirmed_on = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_tenantadmin = models.BooleanField(default=False)
    branch = models.ForeignKey(CompanyInfo, on_delete=models.SET_NULL, null=True, blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ["first_name", "last_name", "email"]
    
    objects = UserManager()



