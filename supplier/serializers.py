from rest_framework import serializers

from .models import Supplier
from .validators import (unique_email, unique_phoneNumber)

class CreateSupplierSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False, allow_blank=True)
    address = serializers.CharField(required=False, allow_blank=True)
    phone_number = serializers.CharField(required=True, allow_blank=False, validators=[unique_phoneNumber])
    email = serializers.EmailField(required=False, allow_blank=True, validators=[unique_email])
   
    class Meta:
        model = Supplier
        fields = '__all__'


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model=Supplier
        fields = '__all__'