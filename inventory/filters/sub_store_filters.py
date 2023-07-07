from django_filters import rest_framework as filters

from inventory.models.sub_store import SubStore


class SubStoreFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="contains")

    class Meta:
        model = SubStore
        fields = ["name"]