from rest_framework import serializers

from inventory.models.inventory_category import InventoryCategory


class InventoryCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryCategory
        fields = "__all__"