from rest_framework import serializers

from authuser.serializers import UserSerializer
from .models import CustomActionLogs

class CustomLogActionSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username")
    class Meta:
        model = CustomActionLogs
        exclude = ['object_id', 'content_type', 'location']