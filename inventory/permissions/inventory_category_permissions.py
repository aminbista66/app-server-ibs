from rest_framework.permissions import BasePermission

class CanViewInventoryCategoryPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('inventory.view_inventorycategory')
        )
    
class CanCreateInventoryCategoryPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('inventory.add_inventorycategory')
        )
    
class CanChangeInventoryCategoryPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('inventory.change_inventorycategory')
        )
    
class CanDeleteInventoryCategoryPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('inventory.delete_inventorycategory')
        )