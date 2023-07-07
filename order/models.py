from django.db import models
from common.models import TimestampsFieldMixin

from companyinfo.models import BranchFieldMixin, CompanyInfo
from customer.models import Customer
from fiscalyear.models import FiscalYear, FiscalYearFieldMixin
from product.models.product import Product
from room.models import BookedRoom, Room
from table.models import Table
from .validator import validate_minimum

class TableOrderQuerySet(models.QuerySet):
    def get_table_order_of_branch(self, branch=None, fiscal_year=None):
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


class TableOrderManager(models.Manager):
    def get_queryset(self):
        return TableOrderQuerySet(self.model, using=self._db)
    
    def get_table_order_of_branch(self, branch=None, fiscal_year=None):
        return self.get_queryset().get_table_order_of_branch(branch,fiscal_year)


class OrderItem(BranchFieldMixin, models.Model):
    quantity = models.PositiveIntegerField(null=False, blank=False, validators=[validate_minimum])
    product = models.ForeignKey(Product, on_delete=models.RESTRICT)

    def str(self):
        return f'{self.product} | {self.quantity}'


class TableOrder(
    BranchFieldMixin, FiscalYearFieldMixin, TimestampsFieldMixin, models.Model
):
    table = models.ForeignKey(Table, on_delete=models.RESTRICT, related_name="table_orders")
    customer = models.ForeignKey(Customer, on_delete=models.RESTRICT, null=True, blank=True)
    products = models.ManyToManyField(Product,)

    objects = TableOrderManager()

    def __str__(self) -> str:
        return self.table.name


class RoomOrderQuerySet(models.QuerySet):
    def get_room_order_of_branch(self, branch=None, fiscal_year=None):
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


class RoomOrderManager(models.Manager):
    def get_queryset(self):
        return RoomOrderQuerySet(self.model, using=self._db)
    
    def get_room_order_of_branch(self, branch=None, fiscal_year=None):
        return self.get_queryset().get_room_order_of_branch(branch,fiscal_year)


class RoomOrder(
    BranchFieldMixin, FiscalYearFieldMixin, TimestampsFieldMixin, models.Model
):
    class OrderStatus(models.TextChoices):
        PENDING = "pending", "Pending"
        SUCCESS = "success", "Success"
        CANCELLED = "cancelled", "Cancelled"
        ISSUED = "issued", "Issued"
        READY = "ready", "Ready"

    # this need to Booked room
    room = models.ForeignKey(Room, on_delete=models.RESTRICT, related_name="room_orders")
    customer = models.ForeignKey(Customer, on_delete=models.RESTRICT, related_name="room_orders")
    order_items = models.ManyToManyField(OrderItem, related_name="order_items", null=True)
    status = models.CharField(max_length=64, choices=OrderStatus.choices, default=OrderStatus.ISSUED)

    objects = RoomOrderManager()

    def __str__(self) -> str:
        return self.room.name


''' signals '''
from django.db.models.signals import post_save

from product.models.ingredient import ProductIngredient
from inventory.models.sub_inventory import SubInventory
from django.db.models import Q

def decrease_store_item(sender, instance: RoomOrder, **kwargs):
    if instance.status == "ready":
        print(instance.order_items.all())
        for order_item in instance.order_items.all():

            order_object = {
                "quantity": order_item.quantity,
                "product_id": order_item.product.id
            }


            ingredients = ProductIngredient.objects.filter(product__id = order_object["product_id"])

            if ingredients.exists():
                for ingredient in ingredients:
                    ingredient : ProductIngredient
                    quantity_to_deduct = ingredient.quantity * order_object['quantity']
                    sub_inventorys = SubInventory.objects.filter(Q(sub_store__id=ingredient.store.id) & Q(item__id=ingredient.item.id))

                    for sub_inventory in sub_inventorys:
                        sub_inventory.quantity -= quantity_to_deduct
                        sub_inventory.save()

post_save.connect(decrease_store_item, sender=RoomOrder)