from django.db import transaction
from rest_framework import serializers
from inventory.exceptions import InvalidSubInventory

from inventory.models.inventory import Inventory
from inventory.models.inventory_item import InventoryItem
from inventory.models.sub_inventory import SubInventory
from inventory.models.sub_store import SubStore


class SubInventorySubStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubStore
        fields = ["id", "name"]

class SubInventoryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryItem
        fields = ["name"]

class SubInventorySerializer(serializers.ModelSerializer):
    sub_store = SubInventorySubStoreSerializer()
    remaining = serializers.SerializerMethodField(read_only=True)
    class Meta: 
        model = SubInventory
        fields = [
            'sub_store',
            'quantity',
            'total_deduction',
            'remaining',
        ]
    def get_remaining(self, obj:SubInventory):
        remaining: float = float(obj.quantity) - float(obj.total_deduction)
        return remaining



''' Measurement unit serializer '''
from ..models.measurement_unit import MeasurementUnit
class MeasurementUnitSerializer(serializers.ModelSerializer):

    class Meta:
        ref_name = "cropped measurementunit serializer"
        model = MeasurementUnit
        fields = [
            "name",
            "code",
            "status",
        ]

class InventoryInventoryItemSerializer(serializers.ModelSerializer):
    measurement_unit = MeasurementUnitSerializer()
    class Meta:
        model = InventoryItem
        fields = ["id", "name", "measurement_unit", "reorder_threshold"]


class InventorySerializer(serializers.ModelSerializer):
    sub_inventories = SubInventorySerializer(many=True, )
    item = InventoryInventoryItemSerializer()

    class Meta:
        model = Inventory
        fields = "__all__" 


class InventoryCreateSerializer(serializers.ModelSerializer):
    sub_inventories = SubInventorySerializer(many=True)
    class Meta:
        model = Inventory
        fields = "__all__"

    def create(self, validated_data):
        with transaction.atomic():
            item = validated_data.get("item", None)
            
            inventory = Inventory.objects.create(**validated_data)
            
            sub_inventories = []
            sub_stores = SubStore.objects.all()
            for sub_store in sub_stores:
                sub_inventory = SubInventory()
                sub_inventory.item = item
                sub_inventory.sub_store = sub_store

                sub_inventory.save()
                sub_inventories.append(sub_inventory)
            
            inventory.sub_inventories.set(sub_inventories)

        return inventory


