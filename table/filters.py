from django_filters import rest_framework as filters
from .models import Table

class TableFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="contains")
    table_category = filters.CharFilter(field_name="table_category", lookup_expr="name__contains")

    class Meta:
        model = Table
        fields = ["table_category", "name"]


