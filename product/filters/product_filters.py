from django_filters import rest_framework as filters

from product.models.product import Product


class ProductFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="contains")
    category = filters.CharFilter(field_name="category", lookup_expr="name__contains")

    class Meta:
        model = Product
        fields = ["name", "category"]