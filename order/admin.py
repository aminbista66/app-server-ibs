from django.contrib import admin
from .models import RoomOrder, TableOrder, OrderItem


admin.site.register(RoomOrder)
admin.site.register(TableOrder)
admin.site.register(OrderItem)