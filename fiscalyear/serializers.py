from rest_framework import serializers
from .models import FiscalYear



class FiscalYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = FiscalYear
        fields = "__all__"
