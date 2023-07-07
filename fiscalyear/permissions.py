from rest_framework.permissions import BasePermission

class CanCreateFiscalYearPermission(BasePermission):
     def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('fiscalyear.add_fiscalyear')
        )


class CanChangeFiscalYearPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('fiscalyear.change_fiscalyear')
        )


class CanViewFiscalYearPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('fiscalyear.view_fiscalyear')
        )


class CanDeleteFiscalYearPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('fiscalyear.delete_fiscalyear')
        )