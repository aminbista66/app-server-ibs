from rest_framework import serializers
from product.models.product_image import ProductImage

class ProductImageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ProductImage
        fields = "__all__"