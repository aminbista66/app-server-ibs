from rest_framework.permissions import BasePermission



class CanCreatePaymentMethodPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('payment.add_paymentmethod')
        )


class CanChangePaymentMethodPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('payment.change_paymentmethod')
        )


class CanDeletePaymentMethodPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('payment.delete_paymentmethod')
        )


class CanViewPaymentMethodPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('payment.view_paymentmethod')
        )