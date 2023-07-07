from django_filters import rest_framework as filters

from invoice.models.purchase_invoice import PurchaseInvoice



class PurchaseInvoiceFilter(filters.FilterSet):
    supplier = filters.CharFilter(field_name="supplier", lookup_expr="name__contains")
    ref_bill_no = filters.CharFilter(field_name="ref_bill_no", lookup_expr="contains")
    created_by = filters.CharFilter(field_name="created_by", lookup_expr="username__contains")
    purchase_date = filters.DateTimeFilter(field_name="purchase_date", lookup_expr="contains")

    class Meta:
        model = PurchaseInvoice
        fields = ["supplier", "ref_bill_no", "created_by", "purchase_date"]