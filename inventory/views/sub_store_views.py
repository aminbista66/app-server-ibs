from rest_framework import generics
from inventory.filters.sub_store_filters import SubStoreFilter
from inventory.models.sub_store import SubStore
from common.permissions import IsTenantAdminOrHasBranchAccessPermission
from inventory.permissions.sub_store_permissions import (
    CanChangeSubStorePermission,
    CanCreateSubStorePermission,
    CanDeleteSubStorePermission,
    CanViewSubStorePermission,
)

from inventory.serializers.sub_store_serializers import SubStoreSerializer
from logs.logs_mixins import CustomCreateAPIView, CustomRetrieveUpdateDeleteAPIView


class SubStoreListAPIView(generics.ListAPIView):
    serializer_class = SubStoreSerializer
    permission_classes = [CanViewSubStorePermission]
    filterset_class = SubStoreFilter

    def get_queryset(self):
        branch = self.request.GET.get("branch", None)
        return SubStore.objects.get_substore_of_branch(branch).order_by("-created_at")


class SubStoreCreateAPIView(CustomCreateAPIView):
    serializer_class = SubStoreSerializer
    permission_classes = [
        IsTenantAdminOrHasBranchAccessPermission,
        CanCreateSubStorePermission,
    ]

    def get_queryset(self):
        branch = self.request.GET.get("branch", None)

        return SubStore.objects.get_substore_of_branch(
            branch,
        )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context


class SubStoreRetrieveUpdateDeleteAPIView(CustomRetrieveUpdateDeleteAPIView):
    serializer_class = SubStoreSerializer

    def get_permissions(self):
        req_method = self.request.method
        if req_method == "GET":
            return [IsTenantAdminOrHasBranchAccessPermission(), CanViewSubStorePermission()]
        elif req_method == "PUT" or req_method == "PATCH":
            return [
                IsTenantAdminOrHasBranchAccessPermission(),
                CanChangeSubStorePermission(),
            ]
        elif req_method == "DELETE":
            return [
                IsTenantAdminOrHasBranchAccessPermission(),
                CanDeleteSubStorePermission(),
            ]
        else:
            return super().get_permissions()

    def get_queryset(self):
        branch = self.request.GET.get("branch", None)
        return SubStore.objects.get_substore_of_branch(
            branch,
        )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context
