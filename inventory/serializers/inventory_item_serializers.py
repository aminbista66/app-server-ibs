from rest_framework import serializers

from inventory.models import InventoryCategory, InventoryItem
from inventory.serializers.inventory_category_serializers import InventoryCategorySerializer
from inventory.serializers.measurement_unit_serializers import MeasurementUnitSerializer

class InventoryItemSerializer(serializers.ModelSerializer):
    category = InventoryCategorySerializer()
    measurement_unit = MeasurementUnitSerializer()
    
    class Meta:
        model = InventoryItem
        fields = "__all__"


class InventoryItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryItem
        fields = "__all__"
