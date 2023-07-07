from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.db import models
from django.contrib.auth.models import Group
from dateutil.relativedelta import relativedelta
from fiscalyear.models import FiscalYear
from tenants.models import Tenant


PLAN_PERIOD_TYPE = (("month", "Month"), ("year", "Year"))


class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100, unique=True)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)
    device_limit = models.IntegerField(default=1)
    branch_limit = models.IntegerField(default=1)
    duration = models.PositiveIntegerField(default=1)
    period_type = models.CharField(
        max_length=10, choices=PLAN_PERIOD_TYPE, default=PLAN_PERIOD_TYPE[1]
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Subscription(models.Model):
    domain = models.CharField(max_length=150)
    is_maintainance = models.BooleanField(default=False)
    group = models.ForeignKey(Group, on_delete=models.RESTRICT, null=True)
    device_limit = models.PositiveIntegerField(default=1)
    device_count = models.PositiveIntegerField(default=0)
    branch_limit = models.IntegerField(default=1)
    is_active = models.BooleanField(default=False)
    expiry_date = models.DateTimeField()
    tenant = models.OneToOneField(Tenant, on_delete=models.RESTRICT)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.domain

    def is_device_limit_reached(self):
        return self.device_count > self.device_limit


class SubscriptionTransaction(models.Model):
    name = models.CharField(max_length=100)
    tenant = models.ForeignKey(Tenant, on_delete=models.RESTRICT)
    subscription_plan = models.ForeignKey(SubscriptionPlan, on_delete=models.RESTRICT)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs) -> None:
        subscriptions = Subscription.objects.using("default").filter(
            tenant=self.tenant.id
        )

        subscription: Subscription = None
        if subscriptions.exists():
            subscription = subscriptions.first()
        else:
            subscription = Subscription()
            tenant = Tenant.objects.using("default").get(pk=self.tenant.id)
            subscription.domain = tenant.subdomain
            subscription.tenant = tenant
            subscription.expiry_date = datetime.today()

        plan = SubscriptionPlan.objects.using("default").get(
            pk=self.subscription_plan.id
        )

        self.amount = plan.price

        subscription.group = plan.group
        subscription.device_limit = plan.device_limit
        subscription.branch_limit = plan.branch_limit
        subscription.is_active = True
        duration = plan.duration
        period_type = plan.period_type

        if period_type == "year":
            subscription.expiry_date = subscription.expiry_date + relativedelta(
                years=duration
            )
        else:
            subscription.expiry_date = subscription.expiry_date + relativedelta(
                months=duration
            )

        subscription.save()

        '''Change permission in tenant's Group after subscription plan has changed'''

        tenant_group, created = Group.objects.using(self.tenant.schema_name).get_or_create(name='Admin Group')
        tenant_admin_permissions = list(subscription.group.permissions.all())
        tenant_group.permissions.remove()
        tenant_group.permissions.set(tenant_admin_permissions)
        tenant_group.save()

        from .utils import permission_filter

        tenant_user_groups = Group.objects.using(self.tenant.schema_name).exclude(name='Admin Group')

        for user_group in tenant_user_groups:
            user_group_permissions = user_group.permissions.all()
            filtered_permissions = permission_filter(user_group_permissions, tenant_admin_permissions)
            user_group.permissions.remove()
            user_group.permissions.set(filtered_permissions)
            user_group.save()

        return super().save(*args, **kwargs)


class DevicesHistory(models.Model):
    fiscal_year = models.ForeignKey(FiscalYear, on_delete=models.RESTRICT, null=True)
    subscription = models.ForeignKey(Subscription, on_delete=models.RESTRICT)
    device_ip = models.CharField(max_length=50)
    location = models.CharField(max_length=50, null=True)
    device_type = models.CharField(max_length=50)
    device_os = models.CharField(max_length=50)
    browser_type = models.CharField(max_length=50)
    device_user = models.CharField(max_length=50)
    refresh_token = models.TextField()
    is_active = models.BooleanField(default=1)
    last_login = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s - %s" % (self.device_ip, self.device_user)

    def save(self, *args, **kwargs):
        fiscal_year = FiscalYear.objects.using("default").filter(is_active=True).first()
        try:
            self.fiscal_year = fiscal_year
        except:
            pass
        super(DevicesHistory, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "device histories"
