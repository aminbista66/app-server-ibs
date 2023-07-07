from rest_framework.permissions import BasePermission


class CanViewPurchaseInvoiceImagePermission(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('invoice.view_purchaseinvoiceimage')
        )
    
class CanCreatePurchaseInvoiceImagePermission(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('invoice.add_purchaseinvoiceimage')
        )
    
class CanChangePurchaseInvoiceImagePermission(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('invoice.change_purchaseinvoiceimage')
        )
    
class CanDeletePurchaseInvoiceImagePermission(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('invoice.delete_purchaseinvoiceimage')
        )