from rest_framework.permissions import BasePermission

class IsTenantAdminOrHasBranchAccessPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_tenantadmin:
            return True
        elif request.user.branch is not None and request.user.branch.id == obj.branch.id:
            return True
        else:
            return False