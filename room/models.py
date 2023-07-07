from django.db import models
from common.models import TimestampsFieldMixin
from common.utils import image_validate
from companyinfo.models import CompanyInfo, BranchFieldMixin
from accounting.models import DiscountRule, TaxRule
from customer.models import Customer

from .utils import get_upload_folder


class RoomCategoryQuerySet(models.QuerySet):
    def get_room_category_of_branch(self, branch=None):
        _branch = (
            branch
            if branch is not None and branch != ""
            else CompanyInfo.objects.first()
        )
        return self.filter(branch=_branch)


class RoomCategoryManager(models.Manager):
    def get_queryset(self):
        return RoomCategoryQuerySet(self.model, using=self._db)

    def get_room_category_of_branch(self, branch=None):
        return self.get_queryset().get_room_category_of_branch(branch)


class RoomCategory(BranchFieldMixin, models.Model):
    class CategoryStatus(models.TextChoices):
        ACTIVE = "active", "Active"
        INACTIVE = "inactive", "Inactive"

    name = models.CharField(max_length=150, unique=True)
    status = models.CharField(
        max_length=15, choices=CategoryStatus.choices, default=CategoryStatus.ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = RoomCategoryManager()

    class Meta:
        verbose_name_plural = "room categories"

    def __str__(self) -> str:
        return self.name


class RoomFeatureQuerySet(models.QuerySet):
    def get_room_feature_of_branch(self, branch=None):
        _branch = (
            branch
            if branch is not None and branch != ""
            else CompanyInfo.objects.first()
        )
        return self.filter(branch=_branch)


class RoomFeatureManager(models.Manager):
    def get_queryset(self):
        return RoomFeatureQuerySet(self.model, using=self._db)

    def get_room_feature_of_branch(self, branch=None):
        return self.get_queryset().get_room_feature_of_branch(branch)


class RoomFeature(BranchFieldMixin, models.Model):
    name = models.CharField(max_length=150, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = RoomFeatureManager()

    def __str__(self) -> str:
        return self.name



class RoomQuerySet(models.QuerySet):
    def get_room_of_branch(self, branch=None):
        _branch = (
            branch
            if branch is not None and branch != ""
            else CompanyInfo.objects.first()
        )
        return self.filter(branch=_branch)


class RoomManager(models.Manager):
    def get_queryset(self):
        return RoomQuerySet(self.model, using=self._db)

    def get_room_of_branch(self, branch=None):
        return self.get_queryset().get_room_of_branch(branch)


class Room(BranchFieldMixin, models.Model):
    class RoomStatus(models.TextChoices):
        FREE = "free", "Free"
        OCCUPIED = "occupied", "Occupied"
        RESERVED = "reserved", "Reserved"

    name = models.CharField(max_length=150, unique=True)
    image = models.ImageField(upload_to=get_upload_folder, validators=[
                              image_validate], null=True, blank=True)
    room_category = models.ForeignKey(RoomCategory, on_delete=models.RESTRICT)
    floor = models.CharField(max_length=50)
    room_status = models.CharField(
        max_length=15, choices=RoomStatus.choices, default=RoomStatus.FREE)
    room_capacity = models.PositiveIntegerField()
    room_features = models.ManyToManyField(RoomFeature)
    include_breakfast = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = RoomManager()

    def __str__(self) -> str:
        return self.name


''' room booking models '''
class BookedRoomQuerySet(models.QuerySet):
    def get_room_of_branch(self, branch=None):
        _branch = (
            branch
            if branch is not None and branch != ""
            else CompanyInfo.objects.first()
        )
        return self.filter(branch=_branch)


class BookedRoomManager(models.Manager):
    def get_queryset(self):
        return BookedRoomQuerySet(self.model, using=self._db)

    def get_room_of_branch(self, branch=None):
        return self.get_queryset().get_room_of_branch(branch)

class BookedRoom(BranchFieldMixin, TimestampsFieldMixin, models.Model):
    class PaymentStatus(models.TextChoices):
        PAID = "paid", "Paid"
        UNPAID = "unpaid", "Unpaid"

    rooms = models.ManyToManyField(Room, related_name="booked_rooms")

    checkin_date = models.DateTimeField(blank=False, null=False)
    checkout_date = models.DateTimeField(blank=False, null=False)
    extended_time = models.DateTimeField(null=True, blank=True)
    extended_period = models.DecimalField(blank=True, null=True,max_digits=4, decimal_places=1, default=0.0)
    # is_occupied = models.BooleanField(default=False)

    # one customer may book multiple room
    customer = models.ForeignKey(Customer, on_delete=models.RESTRICT, null=True)

    adult = models.PositiveIntegerField(blank=False, null=False)
    children = models.PositiveIntegerField(blank=False, null=False)

    payment_status = models.CharField(max_length=12, choices=PaymentStatus.choices, default=PaymentStatus.UNPAID)

    discount_rule = models.ForeignKey(
        DiscountRule, null=True, on_delete=models.SET_NULL, related_name='room_discount_rule')
    tax_rule = models.ForeignKey(
        TaxRule, null=True, on_delete=models.SET_NULL, related_name='room_tax_rule')

    objects = BookedRoomManager()

    def net_stay_price(self):

        def get_days(check_in, check_out):
            from datetime import timedelta
            time_detla: timedelta = check_out - check_in
            return time_detla.days

        total_net_price = 0.0

        for room in self.rooms.all():
            net_room_price = room.price * \
                get_days(self.checkin_date, self.checkout_date)

            if self.discount_rule.status == 'active':
                discount_amount = self.discount_rule.amount
                if self.discount_rule.type == 'percentage':
                    discount_amount = net_room_price * (self.discount_rule.amount / 100)
                net_room_price = net_room_price - discount_amount

            if self.tax_rule.status == 'active':
                net_room_price = net_room_price + net_room_price * (self.tax_rule.rate / 100)
            total_net_price = total_net_price + float(net_room_price)

        return total_net_price

''' Signals '''
from django.db.models.signals import pre_delete

def reset_room_status(sender, instance, **kwargs):
    for room in instance.rooms.all():
        room : Room
        room.room_status = "free"
        room.save()

pre_delete.connect(reset_room_status, sender=BookedRoom)