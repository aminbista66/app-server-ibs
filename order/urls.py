from django.urls import path
from order.views.table_order_views import TableOrderListAPIView, TableOrderCreateAPIView
from order.views.room_order_views import RoomOrderListAPIView, RoomOrderDeleteAPIView, RoomOrderCreateAPIView

urlpatterns = [
    path("tableorders/", TableOrderListAPIView.as_view(), name="table-orders-list"),
    path("tableorders/create/", TableOrderCreateAPIView.as_view(), name="table-orders-list"),

    path("roomorder/", RoomOrderListAPIView.as_view(), name="room-orders-list"),
    path("roomorders/create/", RoomOrderCreateAPIView.as_view(), name="room-orders-create"),
    path("roomorders/delete/<int:pk>/", RoomOrderDeleteAPIView.as_view(), name="room-orders-delete"),
]
