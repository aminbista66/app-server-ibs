
from rest_framework import serializers
from customer.serializers import CustomerSerializer


from order.models import TableOrder
from product.serializers.product_serializers import ProductSerializer
from table.serializers import TableSerializer


class TableOrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TableOrder
        fields = "__all__"



class TableOrderSerializer(serializers.ModelSerializer):
    table = TableSerializer()
    customer = CustomerSerializer()
    product = ProductSerializer(many=True)
    
    class Meta:
        model = TableOrder
        fields = "__all__"