from django.db import models
from common.models import TimestampsFieldMixin

from companyinfo.models import BranchFieldMixin, CompanyInfo
from fiscalyear.models import FiscalYear, FiscalYearFieldMixin
from customer.models import Customer
from room.models import BookedRoom
from product.models.product import Product
from authuser.models import User
from accounting.models import DiscountRule, TaxRule
from order.models import RoomOrder, TableOrder
''' Change this to Booked Table'''
from table.models import Table



class SalesInvoiceQuerySet(models.QuerySet):
    def get_inventory_purchase_history_of_branch(self, branch=None, fiscal_year=None):
        _branch = (
            branch
            if branch is not None and branch != ""
            else CompanyInfo.objects.first()
        )
        _fiscal_year = (
            fiscal_year
            if fiscal_year is not None and fiscal_year != ""
            else FiscalYear.objects.using("default").filter(is_active=True).first()
        )
        return self.filter(branch=_branch, fiscal_year=_fiscal_year)


class SalesInvoiceManager(models.Manager):
    def get_queryset(self):
        return SalesInvoiceQuerySet(self.model, using=self._db)

    def get_inventory_purchase_history_of_branch(self, branch=None, fiscal_year=None):
        return self.get_queryset().get_inventory_purchase_history_of_branch(
            branch, fiscal_year
        )


class SalesInvoice(BranchFieldMixin, TimestampsFieldMixin, FiscalYearFieldMixin, models.Model):
    class PaymentChoice(models.TextChoices):
        UNPAID = 'unpaid', 'Unpaid'
        PAID = 'paid', 'Paid'

    customer = models.ForeignKey(Customer, on_delete=models.RESTRICT, null=True, blank=True)
    booked_room = models.ForeignKey(BookedRoom, on_delete=models.RESTRICT, null=True, blank=True)

    ''' change this to Booked Table'''
    table = models.ForeignKey(Table, on_delete=models.RESTRICT, null=True, blank=True)
    items = models.ManyToManyField(Product, related_name="checkout_invoice")

    ref_bill_no = models.CharField(max_length=50)
    gross_amount = models.DecimalField(max_digits=16, decimal_places=4, default=0.0)

    # net_amount = models.DecimalField(max_digits=16, decimal_places=4, default=0.0)
    created_by = models.ForeignKey(User, on_delete=models.RESTRICT)
    payment_mode = models.CharField(max_length=150)

    payment_status = models.CharField(max_length=48, choices=PaymentChoice.choices, default=PaymentChoice.UNPAID)

    discount_rule = models.ForeignKey(
        DiscountRule, null=True, on_delete=models.SET_NULL, related_name='booked_room_discount_rule')
    tax_rule = models.ForeignKey(
        TaxRule, null=True, on_delete=models.SET_NULL, related_name='booked_room_tax_rule')

    def net_amount(self):
        net_amount = self.gross_amount
        if self.discount_rule.status == 'active':
            discount_amount = self.discount_rule.amount
            if self.discount_rule.type == 'percentage':
                discount_amount = net_amount * (self.discount_rule.amount / 100)
            net_amount -= discount_amount

        if self.tax_rule.status == 'active':
            net_amount = net_amount + net_amount * (self.tax_rule.rate / 100)

        return net_amount

    def calculate_gross_amount(self):
        amount_object = {
            'room_amount': self.booked_room.net_stay_price(),
            'room_order_amount': 0,
            'table_order_amount': 0,
        }
        room_orders = RoomOrder.objects.filter(room__id=self.room.room.id)
        table_orders = TableOrder.objects.filter(table__id=self.table.id)
        if room_orders.exists():
            for room_order in room_orders:
                amount_object['room_order_amount'] += room_order.products.price
        if table_orders.exists():
            for table_order in table_orders:
                amount_object['table_order_amount'] += table_order.products.price
        total_gross_amount = amount_object['room_amount'] + amount_object['room_order_amount'] + amount_object['table_order_amount']
        self.gross_amount = total_gross_amount
        return

    def __str__(self) -> str:
        return f'bill for {self.customer.name}'


'''
    request comes for creating a invoice with cutomer_id or room_id or table_id
    then create SalesInvoice instance and calculate the gross amount then assign
'''