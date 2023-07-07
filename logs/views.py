from django.shortcuts import render


from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination

from .serializers import CustomLogActionSerializer
from .models import CustomActionLogs

class ListActionLogApiView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = LimitOffsetPagination
    serializer_class = CustomLogActionSerializer
    queryset = CustomActionLogs.objects.all()



