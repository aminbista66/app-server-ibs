from rest_framework import serializers

from inventory.models.inventory import Inventory
from inventory.models.inventory_item import InventoryItem
from inventory.models.sub_store import SubStore


class SendToSubStoreSerializer(serializers.Serializer):
    item_id = serializers.IntegerField(required=True)
    sub_store_id = serializers.IntegerField(required=True)
    quantity = serializers.DecimalField(max_digits=12, decimal_places=4, required=True)

    def validate(self, attrs):
        item_id = attrs.get("item_id")
        sub_store_id = attrs.get("sub_store_id")
        quantity = attrs.get("quantity")

        try:
            sub_store = SubStore.objects.get(id=sub_store_id)
        except SubStore.DoesNotExist:
            raise serializers.ValidationError(
                "no sub-store exists for given sub-store id"
            )

        try:
            item = InventoryItem.objects.get(id=item_id)
            try:
                inventory = Inventory.objects.get(item=item)
            except Inventory.DoesNotExist:
                raise serializers.ValidationError(
                    "no inventory exists for given item name", code="invalid_item_id"
                )

            if inventory.quantity < quantity:
                raise serializers.ValidationError(
                    "given quantity is greater than quantity in inventory",
                    code="invalid_quantity",
                )
        except InventoryItem.DoesNotExist:
            raise serializers.ValidationError(
                "no iventory item exists for given item name"
            )

        return attrs
