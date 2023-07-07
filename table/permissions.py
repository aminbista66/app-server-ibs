from rest_framework.permissions import BasePermission


class CanCreateTableCategoryPermission(BasePermission):
     def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('table.add_tablecategory')
        )


class CanChangeTableCategoryPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('table.change_tablecategory')
        )


class CanViewTableCategoryPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('table.view_tablecategory')
        )


class CanDeleteTableCategoryPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('table.delete_tablecategory')
        )
    

class CanCreateTablePermission(BasePermission):
     def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('table.add_table')
        )


class CanChangeTablePermission(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('table.change_table')
        )


class CanViewTablePermission(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('table.view_table')
        )


class CanDeleteTablePermission(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('table.delete_table')
        )