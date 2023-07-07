from rest_framework import serializers
from inventory.models.inventory import Inventory
from inventory.models.sub_inventory import SubInventory
from inventory.models.sub_store import SubStore

from invoice.models.purchase_invoice import PurchaseInvoice
from invoice.models.purchase_invoice_line import PurchaseInvoiceLine
from invoice.serializers.purchase_invoice_image_serializers import (
    PurchaseInvoiceImageSerializer,
)
from supplier.serializers import SupplierSerializer
from inventory.serializers.inventory_item_serializers import InventoryItemSerializer

class PurchaseInvoiceLineSerializer(serializers.ModelSerializer):
    inventory_item = InventoryItemSerializer(read_only=True)
    class Meta:
        model = PurchaseInvoiceLine
        fields = (
            'id', 
            'fiscal_year',
            'created_at',
            'updated_at',
            'quantity',
            'total',
            'branch',
            'invoice',
            'inventory_item',
        )
    
    def get_inventory_item_name(self, obj: PurchaseInvoiceLine):
        return obj.inventory_item.name

    def get_inventory_item_price(self, obj: PurchaseInvoiceLine):
        return obj.inventory_item.unit_price


class PurchaseInvoiceSerializer(serializers.ModelSerializer):
    purchase_invoice_lines = PurchaseInvoiceLineSerializer(many=True, read_only=True)
    invoice_image = PurchaseInvoiceImageSerializer()
    supplier = SupplierSerializer()

    class Meta:
        model = PurchaseInvoice
        fields = [
            "id",
            "invoice_image",
            "supplier",
            "purchase_date",
            "ref_bill_no",
            "gross_amount",
            "tax_vat_amount",
            "discount_amount",
            "net_amount",
            "created_by",
            "branch",
            "fiscal_year",
            "created_at",
            "updated_at",
            "purchase_invoice_lines",
        ]


class PurchaseInvoiceLineCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseInvoiceLine
        fields = ["inventory_item", "quantity", "total"]


class PurchaseInvoiceCreateSerializer(serializers.ModelSerializer):
    purchase_invoice_lines = PurchaseInvoiceLineCreateSerializer(
        many=True, write_only=True
    )

    class Meta:
        model = PurchaseInvoice
        fields = [
            "invoice_image",
            "supplier",
            "purchase_date",
            "ref_bill_no",
            "gross_amount",
            "tax_vat_amount",
            "discount_amount",
            "net_amount",
            "created_by",
            "branch",
            "fiscal_year",
            "purchase_invoice_lines",
        ]

    def validate(self, attrs):
        gross_amount = attrs.get("gross_amount")
        tax_vat_amount = attrs.get("tax_vat_amount")
        discount_amount = attrs.get("discount_amount")
        net_amount = attrs.get("net_amount")
        purchase_invoice_lines = attrs.get("purchase_invoice_lines")

        if gross_amount + tax_vat_amount - discount_amount  != net_amount:
            raise serializers.ValidationError(
                "Discount amount or tax-vat amount or gross amount or net amount is invalid",
                "invalid_data",
            )

        if len(purchase_invoice_lines) < 1:
            raise serializers.ValidationError(
                "No any purchase invoice line given", "empty_purchase_invoice_lines"
            )

        for purchase_invoice_line in purchase_invoice_lines:
            inventory_item = purchase_invoice_line["inventory_item"]
            quantity = purchase_invoice_line["quantity"]
            total = purchase_invoice_line["total"]
            if inventory_item.unit_price * quantity != total:
                raise serializers.ValidationError(
                    f"total amount is invalid in one of purchase invoice lines",
                    code="invalid_purchase_invoice_line",
                )
        return attrs

    def create(self, validated_data):
        purchase_invoice_lines = validated_data.pop("purchase_invoice_lines", [])

        purchase_invoice: PurchaseInvoice = PurchaseInvoice.objects.create(**validated_data)

        for purchase_invoice_line in purchase_invoice_lines:
            inventory_item = purchase_invoice_line["inventory_item"]
            quantity = purchase_invoice_line["quantity"]
            total = purchase_invoice_line["total"]
            branch = purchase_invoice.branch
            fiscal_year = purchase_invoice.fiscal_year

            PurchaseInvoiceLine.objects.create(
                inventory_item=inventory_item,
                quantity=quantity,
                total=total,
                branch=branch,
                fiscal_year=fiscal_year,
                invoice=purchase_invoice,
            )

            try:
                inventory: Inventory = Inventory.objects.get(item=inventory_item)
                inventory.quantity = inventory.quantity + quantity
                inventory.purchased_stock  = inventory.purchased_stock + quantity
                inventory.save()
            except Inventory.DoesNotExist:
                inventory = Inventory()
                inventory.item = inventory_item
                inventory.quantity = quantity
                inventory.purchased_stock = quantity
                inventory.branch = branch
                inventory.fiscal_year = fiscal_year
                inventory.save()

                sub_stores = SubStore.objects.all()
                for sub_store in sub_stores:
                    sub_inventory = SubInventory()
                    sub_inventory.item = inventory_item
                    sub_inventory.sub_store = sub_store
                    sub_inventory.save()

                    inventory.sub_inventories.add(sub_inventory)

        return purchase_invoice
