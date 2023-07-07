from django.contrib import admin
from .models import RoomCategory, RoomFeature, Room, BookedRoom



admin.site.register(Room)
admin.site.register(RoomCategory)
admin.site.register(RoomFeature)
admin.site.register(BookedRoom)