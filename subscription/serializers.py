from rest_framework import serializers

from .models import SubscriptionPlan


def unique_name(value):
    if SubscriptionPlan.objects.using('default').filter(name=value).exists():
        raise serializers.ValidationError("Name already exists")
    return value



class SubscriptionPlanSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100, validators =[unique_name] )
    device_limit = serializers.IntegerField(default=1)
    price = serializers.DecimalField(max_digits=8, decimal_places=2)
   
    class Meta:
        model = SubscriptionPlan
        fields = [
            "id",
            "name",
            "price",
            "device_limit",
            "group"
        ]
        ref_name = "tier"

    def validate(self, attrs):
        return attrs



action_serializer_dict_tier = {
    "create": SubscriptionPlanSerializer,
    "list": SubscriptionPlanSerializer,
    "retrieve":SubscriptionPlanSerializer,
    "destroy":SubscriptionPlanSerializer,
    "update":SubscriptionPlanSerializer,
    "partial_update":SubscriptionPlanSerializer,
}