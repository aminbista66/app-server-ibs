from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.filters import SearchFilter

from .permissions import (
    IsTenantAdminOrIsOfSameBranchPermission,
    CanListCompanyInfoPermission,
    CanDeleteCompanyInfoPermission,
    CanCreateCompanyInfoPermission,
    CanUpdateCompanyInfoPermission,
)
from .models import CompanyInfo
from .serializers import CompanyInfoSerializer
from logs.logs_mixins import CustomCreateAPIView, CustomRetrieveUpdateDeleteAPIView


class CompanyInfoListAPIView(generics.ListAPIView):
    serializer_class = CompanyInfoSerializer
    permission_classes = [CanListCompanyInfoPermission]
    filter_backends = [SearchFilter]
    search_fields = ["name"]

    def get_queryset(self):
        branch = self.request.user.branch
        if self.request.user.is_tenantadmin:
            return CompanyInfo.objects.all()
        elif branch is not None:
            return CompanyInfo.objects.filter(id=branch.id)
        else:
            return CompanyInfo.objects.none()


class CompanyInfoCreateAPIView(CustomCreateAPIView):
    queryset = CompanyInfo.objects.all()
    serializer_class = CompanyInfoSerializer
    permission_classes = [CanCreateCompanyInfoPermission, IsTenantAdminOrIsOfSameBranchPermission]

    def get_queryset(self):
        branch = self.request.user.branch
        if self.request.user.is_tenantadmin:
            return CompanyInfo.objects.all()
        elif branch is not None:
            return CompanyInfo.objects.filter(id=branch.id)
        else:
            return CompanyInfo.objects.none()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context


class CompanyInfoRetrieveUpdateDestroyAPIView(CustomRetrieveUpdateDeleteAPIView):
    serializer_class = CompanyInfoSerializer

    def has_permissions(self):
        if self.request.method == "GET":
            return [CanListCompanyInfoPermission(), IsTenantAdminOrIsOfSameBranchPermission()]
        elif self.request.method == "PUT" or self.request.method == "PATCH":
            return [CanUpdateCompanyInfoPermission(), IsTenantAdminOrIsOfSameBranchPermission()]
        elif self.request.method == "DELETE":
            return [CanDeleteCompanyInfoPermission(), IsTenantAdminOrIsOfSameBranchPermission()]
        else:
            return super().get_permissions()

    def get_queryset(self):
        branch = self.request.GET.get("branch", None)
        if self.request.user.is_tenantadmin:
            return CompanyInfo.objects.all()
        elif branch is not None:
            return CompanyInfo.objects.filter(id=branch.id)
        else:
            return CompanyInfo.objects.none()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context
