from rest_framework.permissions import BasePermission


class CanViewTableOrderPermissions(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('order.view_tableorder')
        )
    

class CanCreateTableOrderPermissions(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('order.add_tableorder')
        )


class CanChangeTableOrderPermissions(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('order.change_tableorder')
        )
    

class CanDeleteTableOrderPermissions(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('order.delete_tableorder')
        )