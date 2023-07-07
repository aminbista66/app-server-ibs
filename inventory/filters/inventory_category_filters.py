from django_filters import rest_framework as filters

from inventory.models.inventory_category import InventoryCategory

class InventoryCategoryFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="contains")
    description = filters.CharFilter(field_name="description", lookup_expr="contains")
    status = filters.CharFilter(field_name="status", lookup_expr="contains")
    
    class Meta:
        model = InventoryCategory
        fields = ["name", "description", "status"]