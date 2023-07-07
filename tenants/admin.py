from django.contrib import admin

from .models import Tenant

class TenantModelAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "schema_name",
        "subdomain"
    ]

admin.site.register(Tenant, TenantModelAdmin)