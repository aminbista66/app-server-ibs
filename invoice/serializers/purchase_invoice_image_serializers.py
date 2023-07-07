from rest_framework import serializers

from invoice.models.purchase_invoice_image import PurchaseInvoiceImage


class PurchaseInvoiceImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseInvoiceImage
        fields = "__all__"
