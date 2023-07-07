from rest_framework import serializers
from .models import Supplier
from rest_framework.response import Response

def unique_email(value):
    if Supplier.objects.filter(email=value).exists():
        raise serializers.ValidationError("email already exists")
    return value

def unique_phoneNumber(value):
    if Supplier.objects.filter(phone_number=value).exists():
        raise serializers.ValidationError("phone number already exists")
    return value