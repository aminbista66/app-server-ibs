from django.contrib import admin
from inventory.models import MeasurementUnit, InventoryCategory, Inventory, SubInventory, InventoryItem, SubStore


# Register your models here.
admin.site.register(MeasurementUnit)
admin.site.register(InventoryCategory)
admin.site.register(InventoryItem)
admin.site.register(Inventory)
admin.site.register(SubInventory)
admin.site.register(SubStore)