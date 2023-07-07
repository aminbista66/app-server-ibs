from rest_framework.permissions import BasePermission        


class CanCreateSupplierPermission(BasePermission):
    def has_permission(self, request, view):
        print(request.user.has_perm('supplier.add_supplier'))
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('supplier.add_supplier')
        )

class CanViewSupplierPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('supplier.view_supplier')
        )

class CanDeleteSupplierPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('supplier.delete_supplier')
        )

class CanChangeSupplierPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('supplier.change_supplier')
        )
