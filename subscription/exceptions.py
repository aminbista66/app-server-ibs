from rest_framework import exceptions, status

class ServiceUnavailable(exceptions.APIException):
    status_code = 503
    default_detail = 'Service temporarily unavailable, try again later.'
    default_code = 'service_unavailable'


class SubscriptionExpired(exceptions.APIException):
    status_code = status.HTTP_402_PAYMENT_REQUIRED
    default_detail = 'Your subscription has expired. Please extend your subscription first.'
    default_code = 'subscription_expired'


class TenantDoesNotExist(exceptions.APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "Tenant doesn't exist."
    default_code = 'tenant_not_found'


class SubscriptionDoesNotExist(exceptions.APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "Subscription doesn't exists."
    default_code = 'subscription_not_found'


class DeviceLimitReached(exceptions.APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "Device limit reached."
    default_code = "exceed_device_limit"