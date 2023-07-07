from rest_framework import serializers
from .models import RoomCategory, RoomFeature, Room, BookedRoom
from accounting.serializers import DiscountRuleSerializer, TaxRuleSerializer


class RoomCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=RoomCategory
        fields="__all__"


class RoomFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model=RoomFeature
        fields="__all__"


class RoomSerializer(serializers.ModelSerializer):
    room_category = RoomCategorySerializer()
    room_features = RoomFeatureSerializer(many=True)
    customer_name = serializers.SerializerMethodField(read_only=True)
    checkin_date = serializers.SerializerMethodField(read_only=True)
    checkout_date = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model=Room
        fields=(
            "id",
            "name",
            "image",
            "room_category",
            "floor",
            "room_status",
            "room_capacity",
            "room_features",
            "include_breakfast",
            "price",
            "created_at",
            "updated_at",
            "customer_name",
            "checkin_date",
            "checkout_date",
            "branch",
        )

    def get_customer_name(self, obj: Room):
        booked = BookedRoom.objects.filter(rooms__id = obj.id)
        if booked.exists():
            return booked.first().customer.name
        return

    def get_checkin_date(self, obj: Room):
        booked = BookedRoom.objects.filter(rooms__id = obj.id)
        if booked.exists():
            return booked.first().checkin_date
        return

    def get_checkout_date(self, obj: Room):
        booked = BookedRoom.objects.filter(rooms__id = obj.id)
        if booked.exists():
            return booked.first().checkout_date
        return

class RoomCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Room
        fields="__all__"


''' Booked Room CURD serializers '''

class BookedRoomSerializer(serializers.ModelSerializer):
    discount_rule = DiscountRuleSerializer()
    tax_rule = TaxRuleSerializer()
    net_stay_price = serializers.SerializerMethodField(read_only=True)
    customer_name = serializers.SerializerMethodField()
    rooms = RoomSerializer(many=True)

    class Meta:
        model = BookedRoom
        fields = [
            'id',
            'rooms',
            'checkin_date',
            'checkout_date',
            'extended_time',
            'extended_period',
            'customer_name',
            'adult',
            'children',
            'discount_rule',
            'tax_rule',
            'net_stay_price',
        ]

    def get_net_stay_price(self, obj: BookedRoom):
        return obj.net_stay_price()

    def get_customer_name(self, obj: BookedRoom):
        return obj.customer.name

class BookedRoomCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookedRoom
        fields = (
            'rooms',
            'checkin_date',
            'checkout_date',
            'extended_time',
            'extended_period',
            'customer',
            'adult',
            'children',
            'discount_rule',
            'tax_rule',
            'branch',
        )

    def create(self, validated_data):
        status = self.context['request'].data.get('status', None)
        for room in validated_data.get('rooms', []):
            room.room_status = status
            room.save()
        '''
            Handle Exception....
        '''
        rooms = validated_data.pop("rooms")
        booked_room: BookedRoom = BookedRoom.objects.create(**validated_data)
        booked_room.rooms.set(rooms)
        return booked_room