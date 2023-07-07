from rest_framework import generics

# from logs.logs_mixins import CustomCreateAPIView, CustomRetrieveUpdateDeleteAPIView

from .models import FiscalYear
from .serializers import FiscalYearSerializer
from .permissions import (
    CanViewFiscalYearPermission,
    # CanCreateFiscalYearPermission,
    # CanChangeFiscalYearPermission,
    # CanDeleteFiscalYearPermission
)


class FiscalYearListAPIView(generics.ListAPIView):
    serializer_class = FiscalYearSerializer
    permission_classes = [CanViewFiscalYearPermission]
    queryset = FiscalYear.objects.using("default").all()


# class FiscalYearCreateAPIView(CustomCreateAPIView):
#     serializer_class = FiscalYearSerializer
#     permission_classes = [CanCreateFiscalYearPermission]
#     queryset = FiscalYear.objects.all()

#     def get_serializer_context(self):
#         context = super().get_serializer_context()
#         context.update({"request": self.request})
#         return context
    

# class FiscalYearRetrieveUpdateDeleteAPIView(CustomRetrieveUpdateDeleteAPIView):
#     serializer_class = FiscalYearSerializer
#     queryset = FiscalYear.objects.all()
    
#     def get_serializer_context(self):
#         context = super().get_serializer_context()
#         context.update({"request": self.request})
#         return context
    
#     def get_permissions(self):
#         req_method = self.request.method
#         if req_method == "GET":
#             return [CanViewFiscalYearPermission()]
#         elif req_method == "PUT" or req_method == "PATCH":
#             return [CanChangeFiscalYearPermission()]
#         elif req_method == "DELETE":
#             return [CanDeleteFiscalYearPermission()]
#         else:
#             return super().get_permissions()