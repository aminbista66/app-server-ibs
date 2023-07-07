from rest_framework import generics
from rest_framework.filters import SearchFilter
from common.permissions import IsTenantAdminOrHasBranchAccessPermission

from logs.logs_mixins import CustomCreateAPIView, CustomRetrieveUpdateDeleteAPIView
from .models import Room, RoomCategory, RoomFeature, BookedRoom
from .permissions import (
    CanViewRoomCategoryPermission,
    CanCreateRoomCategoryPermission,
    CanChangeRoomCategoryPermission,
    CanDeleteRoomCategoryPermission,
    CanViewRoomFeaturePermission,
    CanCreateRoomFeaturePermission,
    CanChangeRoomFeaturePermission,
    CanDeleteRoomFeaturePermission,
    CanViewRoomPermission,
    CanCreateRoomPermission,
    CanChangeRoomPermission,
    CanDeleteRoomPermission,
    CanChangeBookedRoomPermission,
    CanCreateBookedRoomPermission,
    CanDeleteBookedRoomPermission,
    CanViewBookedRoomPermission
)
from .serializers import (
    RoomCategorySerializer,
    RoomFeatureSerializer,
    RoomSerializer,
    RoomCreateSerializer,
    BookedRoomSerializer,
    BookedRoomCreateSerializer
)

from .filters import BookedRoomFilterSet, RoomFilterSet


class RoomCategoryListAPIView(generics.ListAPIView):
    serializer_class = RoomCategorySerializer
    permission_classes = [CanViewRoomCategoryPermission]
    filter_backends = [SearchFilter]
    search_fields = ["name"]

    def get_queryset(self):
        branch = self.request.GET.get("branch", None)
        return RoomCategory.objects.get_room_category_of_branch(branch).order_by(
            "-created_at"
        )


class RoomCategoryCreateAPIView(CustomCreateAPIView):
    serializer_class = RoomCategorySerializer
    permission_classes = [
        IsTenantAdminOrHasBranchAccessPermission,
        CanCreateRoomCategoryPermission,
    ]

    def get_queryset(self):
        branch = self.request.GET.get("branch", None)
        return RoomCategory.objects.get_room_category_of_branch(branch=branch)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context


class RoomCategoryRetrieveUpdateDeleteAPIView(CustomRetrieveUpdateDeleteAPIView):
    serializer_class = RoomCategorySerializer

    def get_permissions(self):
        req_method = self.request.method
        if req_method == "GET":
            return [IsTenantAdminOrHasBranchAccessPermission(), CanViewRoomCategoryPermission()]
        elif req_method == "DELETE":
            return [IsTenantAdminOrHasBranchAccessPermission(), CanDeleteRoomCategoryPermission()]
        elif req_method == "PUT" or req_method == "PATCH":
            return [IsTenantAdminOrHasBranchAccessPermission(), CanChangeRoomCategoryPermission()]
        else:
            return super().get_permissions()

    def get_queryset(self):
        branch = self.request.GET.get("branch", None)
        return RoomCategory.objects.get_room_category_of_branch(branch=branch)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context


class RoomFeatureListAPIView(generics.ListAPIView):
    serializer_class = RoomFeatureSerializer
    permission_classes = [CanViewRoomFeaturePermission]

    def get_queryset(self):
        branch = self.request.GET.get("branch", None)
        return RoomFeature.objects.get_room_feature_of_branch(branch).order_by(
            "-created_at"
        )


class RoomFeatureCreateAPIView(CustomCreateAPIView):
    serializer_class = RoomFeatureSerializer
    permission_classes = [
        IsTenantAdminOrHasBranchAccessPermission,
        CanCreateRoomFeaturePermission,
    ]

    def get_queryset(self):
        branch = self.request.GET.get("branch", None)
        return RoomFeature.objects.get_room_feature_of_branch(branch=branch)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context


class RoomFeatureRetrieveUpdateDeleteAPIView(CustomRetrieveUpdateDeleteAPIView):
    serializer_class = RoomFeatureSerializer

    def get_permissions(self):
        req_method = self.request.method
        if req_method == "GET":
            return [IsTenantAdminOrHasBranchAccessPermission(), CanViewRoomFeaturePermission()]
        elif req_method == "DELETE":
            return [IsTenantAdminOrHasBranchAccessPermission(), CanDeleteRoomFeaturePermission()]
        elif req_method == "PUT":
            return [IsTenantAdminOrHasBranchAccessPermission(), CanChangeRoomFeaturePermission()]
        elif req_method == "PATCH":
            return [IsTenantAdminOrHasBranchAccessPermission(), CanChangeRoomFeaturePermission()]
        else:
            return super().get_permissions()

    def get_queryset(self):
        branch = self.request.GET.get("branch", None)
        return RoomFeature.objects.get_room_feature_of_branch(branch=branch)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context


class RoomListAPIView(generics.ListAPIView):
    serializer_class = RoomSerializer
    permission_classes = [CanViewRoomPermission]
    filterset_class = RoomFilterSet

    def get_queryset(self):
        branch = self.request.GET.get("branch", None)
        return Room.objects.get_room_of_branch(branch).order_by(
            "-created_at"
        )


class RoomCreateAPIView(CustomCreateAPIView):
    serializer_class = RoomCreateSerializer
    permission_classes = [
        IsTenantAdminOrHasBranchAccessPermission,
        CanCreateRoomPermission,
    ]

    def get_queryset(self):
        branch = self.request.GET.get("branch", None)
        return Room.objects.get_room_of_branch(branch=branch)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context


class RoomRetrieveUpdateDeleteAPIView(CustomRetrieveUpdateDeleteAPIView):
    def get_serializer_class(self):
        req_method = self.request.method
        if req_method == "GET" or req_method == "DELETE":
            return RoomSerializer
        elif req_method == "PUT" or req_method == "PATCH":
            return RoomCreateSerializer
        else:
            return super().get_serializer_class()

    def get_permissions(self):
        req_method = self.request.method
        if req_method == "GET":
            return [IsTenantAdminOrHasBranchAccessPermission(), CanViewRoomPermission()]
        elif req_method == "DELETE":
            return [IsTenantAdminOrHasBranchAccessPermission(), CanDeleteRoomPermission()]
        elif req_method == "PUT":
            return [IsTenantAdminOrHasBranchAccessPermission(), CanChangeRoomPermission()]
        elif req_method == "PATCH":
            return [IsTenantAdminOrHasBranchAccessPermission(), CanChangeRoomPermission()]
        else:
            return super().get_permissions()

    def get_queryset(self):
        branch = self.request.GET.get("branch", None)
        return Room.objects.get_room_of_branch(branch=branch)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context




''' Booked Room CRUD API '''
class BookedRoomListAPIView(generics.ListAPIView):
    serializer_class = BookedRoomSerializer
    permission_classes = [CanViewBookedRoomPermission]
    filterset_class = BookedRoomFilterSet

    def get_queryset(self):
        branch = self.request.GET.get('branch', None)
        return BookedRoom.objects.get_room_of_branch(branch=branch).order_by("-created_at")

class BookedRoomCreateAPIView(CustomCreateAPIView):
    serializer_class = BookedRoomCreateSerializer
    permission_classes = [
        IsTenantAdminOrHasBranchAccessPermission,
        CanCreateBookedRoomPermission,
    ]

    def get_queryset(self):
        branch = self.request.GET.get("branch", None)
        return BookedRoom.objects.get_room_of_branch(branch=branch)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

class BookedRoomRetrieveUpdateDeleteAPIView(CustomRetrieveUpdateDeleteAPIView):
    def get_serializer_class(self):
        req_method = self.request.method
        if req_method == "GET" or req_method == "DELETE":
            return BookedRoomSerializer
        elif req_method == "PUT" or req_method == "PATCH":
            return BookedRoomCreateSerializer
        else:
            return super().get_serializer_class()

    def get_permissions(self):
        req_method = self.request.method
        if req_method == "GET":
            return [IsTenantAdminOrHasBranchAccessPermission(), CanViewBookedRoomPermission()]
        elif req_method == "DELETE":
            return [IsTenantAdminOrHasBranchAccessPermission(), CanDeleteBookedRoomPermission()]
        elif req_method == "PUT":
            return [IsTenantAdminOrHasBranchAccessPermission(), CanChangeBookedRoomPermission()]
        elif req_method == "PATCH":
            return [IsTenantAdminOrHasBranchAccessPermission(), CanChangeBookedRoomPermission()]
        else:
            return super().get_permissions()

    def get_queryset(self):
        branch = self.request.GET.get("branch", None)
        return BookedRoom.objects.get_room_of_branch(branch=branch)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context