from rest_framework import serializers

from product.models.ingredient import ProductIngredient
from product.models.product import Product
from product.serializers.product_category_serializers import ProductCategorySerializer
from product.serializers.product_image_serializers import ProductImageSerializer


class ProductIngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductIngredient
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    product_image = ProductImageSerializer()
    category = ProductCategorySerializer()
    product_ingredients = ProductIngredientSerializer(many=True)
    net_price = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        fields = (
            "product_image",
            "name",
            "category",
            "product_ingredients",
            "price",
            "unit",
            "status",
            "tax_status",
            "tax_rule",
            "discount_rule",
            "net_price",
        )

    def get_net_price(self, obj: Product):
        return obj.net_price()


class ProductIngredientCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductIngredient
        fields = [
            "item",
            "store",
            "quantity",
        ]


class ProductCreateSerializer(serializers.ModelSerializer):
    product_ingredients = ProductIngredientCreateSerializer(many=True)

    class Meta:
        model = Product
        fields = [
            "product_image",
            "name",
            "category",
            "price",
            "unit",
            "status",
            "branch",
            "fiscal_year",
            "product_ingredients",
            "tax_status",
            "tax_rule",
            "discount_rule",
        ]

    def validate_product_ingredients(self, value):
        print("product ingredient validation", value)
        if len(value) < 1:
            raise serializers.ValidationError(
                "At least one product ingredient is required"
            )

    def create(self, validated_data):
        print("validated data", validated_data)
        product_ingredients = validated_data.pop("product_ingredients", [])

        product = Product.objects.create(**validated_data)

        for ingredient in product_ingredients:
            print("indgredient", ingredient)

            ProductIngredient.objects.create(
                **ingredient,
                product=product,
                branch=product.branch,
                fiscal_year=product.fiscal_year
            )
        return product
    
    
    def update(self, instance, validated_data):
        product_ingredients = validated_data.pop("product_ingredients", [])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()

        ProductIngredient.objects.filter(product=instance).delete()

        for ingredient in product_ingredients:
            print("indgredient", ingredient)

            ProductIngredient.objects.create(
                **ingredient,
                product=instance,
                branch=instance.branch,
                fiscal_year=instance.fiscal_year
            )

        return instance

