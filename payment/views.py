from rest_framework import generics
from rest_framework.filters import SearchFilter
from common.permissions import IsTenantAdminOrHasBranchAccessPermission

from logs.logs_mixins import CustomCreateAPIView, CustomRetrieveUpdateDeleteAPIView
from .serializers import PaymentMethodSerializer
from .models import PaymentMethod
from .permissions import (
    CanCreatePaymentMethodPermission,
    CanChangePaymentMethodPermission,
    CanDeletePaymentMethodPermission,
    CanViewPaymentMethodPermission,
)


class PaymentMethodListAPIView(generics.ListAPIView):
    serializer_class = PaymentMethodSerializer
    filter_backends = [SearchFilter]
    permission_classes = [IsTenantAdminOrHasBranchAccessPermission, CanViewPaymentMethodPermission]
    search_fields = ["method"]

    def get_queryset(self):
        branch = self.request.GET.get("branch", None)
        return PaymentMethod.objects.get_payment_method_of_branch(branch).order_by("-created_at")


class PaymentMethodCreateAPIView(CustomCreateAPIView):
    serializer_class = PaymentMethodSerializer
    permission_classes = [IsTenantAdminOrHasBranchAccessPermission, CanCreatePaymentMethodPermission]

    def get_queryset(self):
        branch = self.request.GET.get("branch", None)
        return PaymentMethod.objects.get_payment_method_of_branch(branch)
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context
    

class PaymentMethodRetrieveUpdateDeleteAPIView(CustomRetrieveUpdateDeleteAPIView):
    serializer_class = PaymentMethodSerializer

    def get_permissions(self):
        req_method = self.request.method
        if req_method == "GET":
            return [IsTenantAdminOrHasBranchAccessPermission(), CanViewPaymentMethodPermission()]
        elif req_method == "DELETE":
            return [IsTenantAdminOrHasBranchAccessPermission(), CanDeletePaymentMethodPermission()]
        elif req_method == "PUT" or req_method == "PATCH":
            return [IsTenantAdminOrHasBranchAccessPermission(), CanChangePaymentMethodPermission()]
        else:
            return super().get_permissions()

    def get_queryset(self):
        branch = self.request.GET.get("branch", None)
        return PaymentMethod.objects.get_payment_method_of_branch(branch)
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context