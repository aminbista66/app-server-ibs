from rest_framework.permissions import BasePermission


class CanViewPurchaseInvoicePermission(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('invoice.view_purchaseinvoice') and
            request.user.has_perm('invoice.view_purchaseinvoiceline')
        )
    
class CanCreatePurchaseInvoicePermission(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('invoice.add_purchaseinvoice') and
            request.user.has_perm('invoice.add_purchaseinvoiceline')
        )
    
class CanChangePurchaseInvoicePermission(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('invoice.change_purchaseinvoice') and
            request.user.has_perm('invoice.change_purchaseinvoiceline')
        )
    
class CanDeletePurchaseInvoicePermission(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('invoice.delete_purchaseinvoice') and
            request.user.has_perm('invoice.delete_purchaseinvoiceline')
        )