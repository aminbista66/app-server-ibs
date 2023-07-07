from typing import Any
from django.contrib import admin
from django.http.request import HttpRequest
from .models import SubscriptionPlan, Subscription, SubscriptionTransaction, DevicesHistory



class SubscriptionPlanModel(admin.ModelAdmin):
    list_display = [
        "name",
        "group",
        "device_limit",
        "branch_limit",
        "duration",
        "period_type",
        "price"
    ]
    list_filter = [
        "name",
        "device_limit",
        "branch_limit",
        "duration",
        "period_type",
        "price"
    ]

    search_fields = ["name"]

# Register your models here.
admin.site.register(SubscriptionPlan, SubscriptionPlanModel)


class SubscriptionModel(admin.ModelAdmin):
    list_display = [
        "domain",
        "tenant",
        "device_count",
        "device_limit",
        "branch_limit",
        "is_active",
        "is_maintainance",
        "expiry_date",
        "group",
        "created_at",
        "update_at",
    ]
    list_filter = [
        "is_maintainance",
        "device_limit",
        "device_count",
        "branch_limit",
        "is_active",
        "expiry_date",
        "created_at",
        "update_at",
    ]

    # def save_model(self, request: HttpRequest, obj: Any, form: Any, change: Any) -> None:
        # super().save_model(request, obj, form, change)
        # from tenants.models import Tenant
        # from django.contrib.auth.models import Group, Permission
        # '''
        #     override for subscription change of tenant
        # '''
        # if not change:
        #     return

        # tenants = Tenant.objects.filter(id=obj.id)
        # if tenants.exists():
        #     tenant = tenants.first()
        #     try:
        #         subscription_group = Group.objects.using('default').get(name=obj.group.name)
                
        #     except Exception as e:
        #         print(e)

admin.site.register(Subscription, SubscriptionModel)

class SubscriptionTransactionModel(admin.ModelAdmin):
    list_display = [
        "name",
        "tenant",
        "subscription_plan",
        "amount",
        "created_at",
    ]
    list_filter = [
        "name",
        "tenant",
        "subscription_plan",
        "created_at",
    ]
    search_fields = ["name"]

admin.site.register(SubscriptionTransaction, SubscriptionTransactionModel)

class DevicesHistoryModel(admin.ModelAdmin):
    list_display = [
        "device_user",
        "device_ip",
        "location",
        "browser_type",
        "device_type",
        "device_os",
        "is_active",
        "last_login",
    ]
    list_filter = ["device_ip", "device_user"]
    search_fields = ["device_ip", "device_user"]

admin.site.register(DevicesHistory, DevicesHistoryModel)