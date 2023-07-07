from rest_framework import generics
from rest_framework.filters import SearchFilter
from common.permissions import IsTenantAdminOrHasBranchAccessPermission

from logs.logs_mixins import CustomCreateAPIView, CustomRetrieveUpdateDeleteAPIView
from .permissions import (
    CanChangeDiscountRulePermission,
    CanCreateDiscountRulePermission,
    CanViewDiscountRulePermission,
    CanDeleteDiscountRulePermission,
    CanViewTaxRulePermission,
    CanChangeTaxRulePermission,
    CanCreateTaxRulePermission,
    CanDeleteTaxRulePermission,
)
from .models import TaxRule, DiscountRule
from .serializers import TaxRuleSerializer, DiscountRuleSerializer


class TaxRuleListAPIView(generics.ListAPIView):
    permission_classes = [IsTenantAdminOrHasBranchAccessPermission, CanViewTaxRulePermission]
    serializer_class = TaxRuleSerializer
    filter_backends = [SearchFilter]
    search_fields = ["name"]

    def get_queryset(self):
        branch = self.request.GET.get("branch", None)
        fiscal_year = self.request.GET.get("fiscal_year", None)
        return TaxRule.objects.get_tax_rule_of_branch(branch, fiscal_year).order_by(
            "-created_at"
        )
    
class TaxRuleCreateAPIView(CustomCreateAPIView):
    permission_classes = [IsTenantAdminOrHasBranchAccessPermission, CanCreateTaxRulePermission]
    serializer_class = TaxRuleSerializer

    def get_queryset(self):
        branch = self.request.GET.get("branch", None)
        fiscal_year = self.request.GET.get("fiscal_year", None)
        return TaxRule.objects.get_tax_rule_of_branch(branch, fiscal_year)
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context
    

class TaxRuleRetrieveUpdateDeleteAPIView(CustomRetrieveUpdateDeleteAPIView):
    serializer_class = TaxRuleSerializer
    
    def get_permissions(self):
        req_method = self.request.GET.get("branch", None)
        if req_method == "GET":
            return [CanViewTaxRulePermission(), IsTenantAdminOrHasBranchAccessPermission()]
        elif req_method == "PUT" or req_method == "PATCH":
            return [
                CanChangeTaxRulePermission(),
                IsTenantAdminOrHasBranchAccessPermission(),
            ]
        elif req_method == "DELETE":
            return [
                CanDeleteTaxRulePermission(),
                IsTenantAdminOrHasBranchAccessPermission(),
            ]
        else:
            return super().get_permissions()

    def get_queryset(self):
        branch = self.request.GET.get("branch", None)
        fiscal_year = self.request.GET.get("fiscal_year", None)
        return TaxRule.objects.get_tax_rule_of_branch(branch, fiscal_year)
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context
    

class DiscountRuleListAPIView(generics.ListAPIView):
    permission_classes = [IsTenantAdminOrHasBranchAccessPermission, CanViewDiscountRulePermission]
    serializer_class = DiscountRuleSerializer
    filter_backends = [SearchFilter]
    search_fields = ["name"]

    def get_queryset(self):
        branch = self.request.GET.get("branch", None)
        fiscal_year = self.request.GET.get("fiscal_year", None)
        return DiscountRule.objects.get_discount_rule_of_branch(branch, fiscal_year).order_by(
            "-created_at"
        )
    
class DiscountRuleCreateAPIView(CustomCreateAPIView):
    permission_classes = [IsTenantAdminOrHasBranchAccessPermission, CanCreateDiscountRulePermission]
    serializer_class = DiscountRuleSerializer

    def get_queryset(self):
        branch = self.request.GET.get("branch", None)
        fiscal_year = self.request.GET.get("fiscal_year", None)
        return DiscountRule.objects.get_discount_rule_of_branch(branch, fiscal_year)
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context
    

class DiscountRuleRetrieveUpdateDeleteAPIView(CustomRetrieveUpdateDeleteAPIView):
    serializer_class = DiscountRuleSerializer
    
    def get_permissions(self):
        req_method = self.request.method
        if req_method == "GET":
            return [CanViewDiscountRulePermission(), IsTenantAdminOrHasBranchAccessPermission()]
        elif req_method == "PUT" or req_method == "PATCH":
            return [
                CanChangeDiscountRulePermission(),
                IsTenantAdminOrHasBranchAccessPermission(),
            ]
        elif req_method == "DELETE":
            return [
                CanDeleteDiscountRulePermission(),
                IsTenantAdminOrHasBranchAccessPermission(),
            ]
        else:
            return super().get_permissions()

    def get_queryset(self):
        branch = self.request.GET.get("branch", None)
        fiscal_year = self.request.GET.get("fiscal_year", None)
        return DiscountRule.objects.get_discount_rule_of_branch(branch, fiscal_year)
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context