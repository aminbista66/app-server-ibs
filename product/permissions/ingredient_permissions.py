from rest_framework.permissions import BasePermission



class CanViewProductIngredientPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('product.view_productingredient')
        )
    
class CanCreateProductIngredientPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('product.add_productingredient')
        )
    
class CanChangeProductIngredientPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('product.change_productingredient')
        )
    
class CanDeleteProductIngredientPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('product.delete_productingredient')
        )