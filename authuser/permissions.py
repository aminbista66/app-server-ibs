from rest_framework.permissions import BasePermission

# user permission
class CanCreateUserPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('authuser.add_user')
        )


class CanViewUserPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('authuser.view_user')
        )


class CanChangeUserPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('authuser.change_user')
        )

class CanDeleteUserPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('authuser.delete_user')
        )


#group permission 
class CanCreateGroupPermission(BasePermission):
    def has_permission(self, request, view):
        return bool (
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('auth.add_group')
        )  


class CanViewGroupPermission(BasePermission):
    def has_permission(self, request, view):  
        print(request.user.has_perm('auth.view_group'))
        return bool (
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('auth.view_group')
        )


class CanDeleteGroupPermission(BasePermission):
    def has_permission(self, request, view):  
        return bool (
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('auth.delete_group')
        )  


class CanChangeGroupPermission(BasePermission):
    def has_permission(self, request, view):  
        return bool (
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('auth.change_group')
        )  
        