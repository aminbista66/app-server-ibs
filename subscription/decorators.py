from datetime import datetime, timezone
from functools import wraps
from rest_framework.response import Response
from rest_framework import status

from .exceptions import ServiceUnavailable, SubscriptionDoesNotExist, TenantDoesNotExist, SubscriptionExpired
from .models import Subscription
from tenants.models import Tenant
from tenants.utils import hostname_from_request


def check_subscription_expiry(view_func):
    @wraps(view_func)
    def wrapper(self, request, *args, **kwargs):
        
        subdomain = hostname_from_request(request)
        tenants = Tenant.objects.using("default").filter(subdomain=subdomain)

        if tenants.exists():
            tenant = tenants.first()

            Subscriptions = Subscription.objects.using("default").filter(tenant=tenant)
            if Subscriptions.exists():
                subscription = Subscriptions.first()
                if subscription.is_maintainance == True:
                    raise ServiceUnavailable()
                
            else:
                raise SubscriptionDoesNotExist()

            if not subscription.is_active:
                raise SubscriptionExpired()
            
            current_date = datetime.now()
            current_date = current_date.replace(tzinfo=timezone.utc)
            if subscription.expiry_date < current_date:
                subscription.is_active = False
                subscription.save(using='default')

                raise SubscriptionExpired()
        else:
            raise TenantDoesNotExist()

        return view_func(self, request, *args, **kwargs)

    return wrapper


