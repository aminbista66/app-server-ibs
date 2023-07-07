from rest_framework import serializers
from .models import TableCategory, Table


class TableCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TableCategory
        fields = "__all__"


class TableSerializer(serializers.ModelSerializer):
    table_category = TableCategorySerializer()
    class Meta:
        model = Table
        fields = "__all__"


class TableCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = "__all__"

