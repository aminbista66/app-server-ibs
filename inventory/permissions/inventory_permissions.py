from rest_framework.permissions import BasePermission


class CanViewInventoryPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('inventory.view_inventory')
        )
    
class CanCreateInventoryPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('inventory.add_inventory')
        )
    
class CanChangeInventoryPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('inventory.change_inventory')
        )
    
class CanDeleteInventoryPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('inventory.delete_inventory')
        )