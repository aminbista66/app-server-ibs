'''
    request comes with product_id, room_id or table_id and customer_id
    get the ingedretiens required for the products from the Product Ingredient model ing = ProductIngredient.objects.get(product=product_id)
    ing = {
        store: 'kitchen',
        quantity: '34',
        item: 'flour',
        product: 'burger'
    }
    get the substore ( i.e  kitchen ) reduce the quantity of item the store kitchen.... 
'''

from rest_framework import generics
from logs.logs_mixins import CustomDeleteAPIView
from ..models import RoomOrder
from ..serializers.room_order_serializer import RoomOrderSerializer, RoomOrderCreateSerializer
from ..permissions.room_order_permissions import (
    CanChangeRoomOrderPermission,
    CanCreateRoomOrderPermission,
    CanDeleteRoomOrderPermission,
    CanViewRoomOrderPermission
)
from logs.logs_mixins import CustomCreateAPIView
from common.permissions import IsTenantAdminOrHasBranchAccessPermission
from ..models import RoomOrder
# Room Order CRUD 

class RoomOrderListAPIView(generics.ListAPIView):
    serializer_class = RoomOrderSerializer
    permission_classes = [CanViewRoomOrderPermission, IsTenantAdminOrHasBranchAccessPermission]

    def get_queryset(self):
        branch = self.request.query_params.get("branch", None)
        fiscal_year = self.request.query_params.get("fiscal_year", None)
        return RoomOrder.objects.get_room_order_of_branch(
            branch, fiscal_year
        ).order_by("-created_at")

class RoomOrderCreateAPIView(CustomCreateAPIView):
    permission_classes = [CanCreateRoomOrderPermission, IsTenantAdminOrHasBranchAccessPermission]
    serializer_class = RoomOrderCreateSerializer

    def get_queryset(self):
        branch = self.request.GET.get("branch", None)
        return RoomOrder.objects.get_room_of_branch(branch=branch)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

class RoomOrderDeleteAPIView(CustomDeleteAPIView):
    def get_serializer_class(self):
        method = self.request.method
        if method == "GET" or method == "DELETE":
            return RoomOrderSerializer
        else:
            return ...

    def get_permissions(self):
        method = self.request.method

        if method == "GET":
            return [
                IsTenantAdminOrHasBranchAccessPermission(),
                CanViewRoomOrderPermission(),
            ]
        elif method == "PUT" or method == "PATCH":
            return [
                IsTenantAdminOrHasBranchAccessPermission(),
                CanChangeRoomOrderPermission(),
            ]
        elif method == "DELETE":
            return [
                IsTenantAdminOrHasBranchAccessPermission(),
                CanDeleteRoomOrderPermission(),
            ]
        else:
            return super().get_permissions()

    def get_queryset(self):
        branch = self.request.query_params.get("branch", None)
        fiscal_year = self.request.query_params.get("fiscal_year", None)
        return RoomOrder.objects.get_room_order_of_branch(branch, fiscal_year)
