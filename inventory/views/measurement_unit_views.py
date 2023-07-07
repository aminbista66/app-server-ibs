from rest_framework import generics
from inventory.filters.mesurement_unit_filters import MeasurementUnitFilter
from inventory.models.measurement_unit import MeasurementUnit
from common.permissions import IsTenantAdminOrHasBranchAccessPermission
from inventory.permissions.measurement_unit_permissions import (
    CanChangeMeasurementUnitPermission,
    CanCreateMeasurementUnitPermission,
    CanDeleteMeasurementUnitPermission,
    CanViewMeasurementUnitPermission,
)

from inventory.serializers.measurement_unit_serializers import MeasurementUnitSerializer
from logs.logs_mixins import CustomCreateAPIView, CustomRetrieveUpdateDeleteAPIView


class MeasurementUnitListAPIView(generics.ListAPIView):
    serializer_class = MeasurementUnitSerializer
    permission_classes = [CanViewMeasurementUnitPermission]
    filterset_class = MeasurementUnitFilter

    def get_queryset(self):
        branch = self.request.GET.get("branch", None)
        fiscal_year = self.request.GET.get("fiscal_year", None)
        return MeasurementUnit.objects.get_measurement_unit_of_branch(
            branch, fiscal_year
        ).order_by("-created_at")


class MeasurementUnitCreateAPIView(CustomCreateAPIView):
    serializer_class = MeasurementUnitSerializer
    permission_classes = [
        IsTenantAdminOrHasBranchAccessPermission,
        CanCreateMeasurementUnitPermission,
    ]

    def get_queryset(self):
        branch = self.request.GET.get("branch", None)
        fiscal_year = self.request.GET.get("fiscal_year", None)
        return MeasurementUnit.objects.get_measurement_unit_of_branch(
            branch, fiscal_year
        )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context


class MeasurementUnitRetrieveUpdateDeleteAPIView(CustomRetrieveUpdateDeleteAPIView):
    serializer_class = MeasurementUnitSerializer

    def get_permissions(self):
        req_method = self.request.method
        if req_method == "GET":
            return [IsTenantAdminOrHasBranchAccessPermission(), CanViewMeasurementUnitPermission()]
        elif req_method == "PUT" or req_method == "PATCH":
            return [
                IsTenantAdminOrHasBranchAccessPermission(),
                CanChangeMeasurementUnitPermission(),
            ]
        elif req_method == "DELETE":
            return [
                IsTenantAdminOrHasBranchAccessPermission(),
                CanDeleteMeasurementUnitPermission(),
            ]
        else:
            return super().get_permissions()

    def get_queryset(self):
        branch = self.request.GET.get("branch", None)
        fiscal_year = self.request.GET.get("fiscal_year", None)
        return MeasurementUnit.objects.get_measurement_unit_of_branch(
            branch, fiscal_year
        )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context
