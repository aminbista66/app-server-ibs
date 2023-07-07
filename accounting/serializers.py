from rest_framework import serializers

from .models import TaxRule, DiscountRule


class TaxRuleSerializer(serializers.ModelSerializer):

    class Meta:
        model = TaxRule
        fields = "__all__"


class DiscountRuleSerializer(serializers.ModelSerializer):

    class Meta:
        model = DiscountRule
        fields = "__all__"