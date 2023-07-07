from rest_framework.permissions import BasePermission


class CanViewInventoryItemPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('inventory.view_inventoryitem')
        )
    
class CanCreateInventoryItemPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('inventory.add_inventoryitem')
        )
    
class CanChangeInventoryItemPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('inventory.change_inventoryitem')
        )
    
class CanDeleteInventoryItemPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('inventory.delete_inventoryitem')
        )