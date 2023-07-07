from django.db import models


class Tenant(models.Model):
    name = models.CharField(max_length=100) 
    schema_name = models.CharField(max_length=100) 
    subdomain = models.CharField(max_length=1000, unique=True)

    def __str__(self):
        return self.name