from rest_framework.permissions import BasePermission


#  tax rule permissions
class CanViewTaxRulePermission(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('accounting.view_taxrule')
        )
    
class CanCreateTaxRulePermission(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('accounting.add_taxrule')
        )
    
class CanChangeTaxRulePermission(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('accounting.change_taxrule')
        )
    
class CanDeleteTaxRulePermission(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('accounting.delete_taxrule')
        )
# end tax rule permissions

# discount rule permissions
class CanViewDiscountRulePermission(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('accounting.view_discountrule')
        )
    
class CanCreateDiscountRulePermission(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('accounting.add_discountrule')
        )
    
class CanChangeDiscountRulePermission(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('accounting.change_discountrule')
        )
    
class CanDeleteDiscountRulePermission(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('accounting.delete_discountrule')
        )
# end discount rule permissions