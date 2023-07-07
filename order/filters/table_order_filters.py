from django_filters import rest_framework as filters
from order.models import TableOrder


class TableOrderFilter(filters.FilterSet):
    table = filters.CharFilter(field_name="table", lookup_expr="name__contains")
    customer = filters.CharFilter(field_name="customer", lookup_expr="name__contains")
    product = filters.CharFilter(field_name="products", lookup_expr="name__contains")

    class Meta:
        model = TableOrder
        fields = ["table", "customer", "product"]