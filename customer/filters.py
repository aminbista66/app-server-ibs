from django_filters import rest_framework as filters

from customer.models import Customer



class CustomerFilter(filters.FilterSet):
    phone = filters.CharFilter(field_name="phone1", lookup_expr="contains")
    
    class Meta:
        model = Customer
        fields = ["phone"]