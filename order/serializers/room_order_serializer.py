from rest_framework import serializers
from ..models import RoomOrder, OrderItem
from room.serializers import RoomSerializer
from product.serializers.product_serializers import ProductSerializer
from product.models.product import Product
from companyinfo.models import CompanyInfo

class OrderItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = (
            "quantity",
            "product",
        )

class RoomOrderSerializer(serializers.ModelSerializer):
    room = RoomSerializer()
    order_items = OrderItemsSerializer(many=True,)
    class Meta:
        model = RoomOrder
        fields = "__all__"

class RoomOrderCreateSerializer(serializers.ModelSerializer):
    order_items = OrderItemsSerializer(many=True)

    class Meta:
        model = RoomOrder
        fields = (
            "id",
            "customer",
            "room",
            "status",
            "branch",
            "fiscal_year",
            "order_items",
        )

    def create(self, validated_data):
        products = validated_data.pop("order_items", [])

        room_order: RoomOrder = RoomOrder.objects.create(**validated_data, )

        for product in products:
            ''' get_or_create '''
            order_item = OrderItem.objects.create(
                branch=validated_data.get("branch"),
                quantity=product.get("quantity"),
                product=Product.objects.get(id=product.get("product").id)
            )
            room_order.order_items.add(order_item)
        return room_order