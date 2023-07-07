from django_filters import rest_framework as filters

from inventory.models.inventory_item import InventoryItem

class InventoryItemFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="contains")
    category = filters.CharFilter(field_name="category", lookup_expr="name__contains")
    status = filters.CharFilter(field_name="status", lookup_expr="contains")
    
    class Meta:
        model = InventoryItem
        fields = ["name", "category", "status"]