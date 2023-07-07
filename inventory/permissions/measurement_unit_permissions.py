from rest_framework.permissions import BasePermission

class CanViewMeasurementUnitPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('inventory.view_measurementunit')
        )
    
class CanCreateMeasurementUnitPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('inventory.add_measurementunit')
        )
    
class CanChangeMeasurementUnitPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('inventory.change_measurementunit')
        )
    
class CanDeleteMeasurementUnitPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('inventory.delete_measurementunit')
        )