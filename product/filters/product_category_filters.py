from django_filters import rest_framework as filters
from product.models.product_category import ProductCategory


class ProductCategoryFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="contains")
    
    class Meta:
        model= ProductCategory
        fields = ["name"]