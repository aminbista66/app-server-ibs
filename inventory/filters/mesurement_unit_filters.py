from django_filters import rest_framework as filters

from inventory.models.measurement_unit import MeasurementUnit

class MeasurementUnitFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="contains")

    class Meta:
        model = MeasurementUnit
        fields = ["name"]