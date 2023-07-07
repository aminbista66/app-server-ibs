from rest_framework.permissions import BasePermission


class IsTenantAdminOrIsOfSameBranchPermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        branch = request.user.branch
        if request.user.is_tenantadmin:
            return True
        elif branch is not None and obj.id == branch.id:
            return True
        else:
            return False
    

class CanCreateCompanyInfoPermission(BasePermission):
    def has_permission(self, request, view):
        return bool (
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('companyinfo.add_companyinfo')
        )    
    
class CanListCompanyInfoPermission(BasePermission):
    def has_permission(self, request, view):
        return bool (
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('companyinfo.view_companyinfo')
        )        

class CanUpdateCompanyInfoPermission(BasePermission):
    def has_permission(self, request, view):
        return bool (
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('companyinfo.change_companyinfo')
        )    
    
class CanDeleteCompanyInfoPermission(BasePermission):
    def has_permission(self, request, view):
        return bool (
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('companyinfo.delete_companyinfo')
        )        