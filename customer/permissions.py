from rest_framework.permissions import BasePermission


class CanCreateCustomerPermission(BasePermission):
     def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('customer.add_customer')
        )


class CanChangeCustomerPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('customer.change_customer')
        )


class CanViewCustomerPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('customer.view_customer')
        )


class CanDeleteCustomerPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('customer.delete_customer')
        )