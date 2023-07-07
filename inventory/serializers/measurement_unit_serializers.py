from rest_framework import serializers

from inventory.models.measurement_unit import MeasurementUnit


class MeasurementUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeasurementUnit
        fields = "__all__"