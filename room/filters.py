from django_filters import rest_framework
from .models import BookedRoom, Room

class BookedRoomFilterSet(rest_framework.FilterSet):
    room_name = rest_framework.CharFilter(field_name='room__name', lookup_expr='icontains')
    customer_name = rest_framework.CharFilter(field_name='customer__name', lookup_expr='icontains')

    class Meta:
        model = BookedRoom
        fields = ['room_name', 'customer_name']

class RoomFilterSet(rest_framework.FilterSet):
    room_name = rest_framework.CharFilter(field_name='room__name', lookup_expr='icontains')
    room_category = rest_framework.CharFilter(field_name='room_category__name', lookup_expr='icontains')

    class Meta:
        model = Room
        fields = ['room_name', 'room_category']