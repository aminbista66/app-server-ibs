from django_filters import rest_framework as filters

from inventory.models.inventory import Inventory


class InventoryFilter(filters.FilterSet):
    item = filters.CharFilter(field_name="item", lookup_expr="name__contains")

    class Meta:
        model = Inventory
        fields = ["item"]