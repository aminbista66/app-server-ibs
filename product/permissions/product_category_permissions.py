from rest_framework.permissions import BasePermission


class CanViewProductCategoryPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('product.view_productcategory')
        )
    
class CanCreateProductCategoryPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('product.add_productcategory')
        )
    
class CanChangeProductCategoryPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('product.change_productcategory')
        )
    
class CanDeleteProductCategoryPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('product.delete_productcategory')
        )