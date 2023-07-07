from rest_framework import serializers

from inventory.models.sub_store import SubStore


class SubStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubStore
        fields = "__all__"

from django.contrib.auth.models import AnonymousUser