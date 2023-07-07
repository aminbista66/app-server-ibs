from django.db import transaction
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from authuser.models import User
from common.utils import image_validate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from subscription.models import Subscription

from tenants.utils import hostname_from_request


class PermissionSerializer(serializers.ModelSerializer):
    content_type = serializers.CharField(source="content_type.name")

    class Meta:
        model = Permission
        fields = "__all__"


class GroupSerializer(serializers.ModelSerializer):
    # name= serializers.CharField(max_length=200)
    permissions = PermissionSerializer(read_only=True, many=True)

    class Meta:
        model = Group
        fields = "__all__"


class CreateGroupSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=150)

    class Meta:
        model = Group
        fields = ["id", "name", "permissions"]

    def create(self, validated_data):
        with transaction.atomic():
            permissions = validated_data.pop("permissions")
            group = Group.objects.create(**validated_data)
            group.permissions.set([per for per in permissions])
        return group

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        permissions = validated_data.get("permissions", instance.permissions.all())
        instance.save()
        instance.permissions.set([i for i in permissions])
        return instance

    def validate(self, attrs):
        request = self.context["request"]
        subdomain = hostname_from_request(request)
        subscription = Subscription.objects.using("default").get(domain=subdomain)
        group = Group.objects.using("default").get(id=subscription.group_id)
        tenant_permissions = Permission.objects.using("default").filter(group=group)

        permissons = attrs["permissions"]

        for perm in permissons:
            if not perm in tenant_permissions:
                raise serializers.ValidationError(
                    "Permission not included in tenant permissions",
                    params={"value": perm},
                )

        return super().validate(attrs)


class UserSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "image",
            "is_superuser",
            "username",
            "first_name",
            "is_active",
            "last_name",
            "last_login",
            "email",
            "groups",
            "is_tenantadmin",
        ]


def unique_username(value):
    if User.objects.filter(username=value).exists():
        raise serializers.ValidationError("username already exists")
    return value


def unique_email(value):
    if User.objects.filter(email=value).exists():
        raise serializers.ValidationError("email already exists")
    return value


class UserCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    image = serializers.ImageField(required=False, validators=[image_validate])
    first_name = serializers.CharField(required=True, max_length=200, allow_blank=False)
    last_name = serializers.CharField(required=True, max_length=200, allow_blank=False)
    username = serializers.CharField(
        required=True, allow_blank=False, validators=[unique_username]
    )
    email = serializers.EmailField(
        required=True, allow_blank=False, validators=[unique_email]
    )
    password = serializers.CharField(
        max_length=100, required=True, allow_blank=False, write_only=True
    )
    group = serializers.IntegerField(required=True, write_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "image",
            "first_name",
            "last_name",
            "username",
            "password",
            "branch",
            "group",
        ]

    def create(self, validated_data):
        with transaction.atomic():
            group = validated_data.pop("group", None)
            groups = Group.objects.filter(pk=group)

            if groups.exists():
                group_object = groups.first()

                user = User.objects.create_user(**validated_data)
                user.save()
                user.groups.set([group_object])

                return user

            else:
                raise serializers.ValidationError("Group with given id does not exist")

    def validate(self, attrs):
        return attrs


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=255, allow_null=False, allow_blank=False
    )
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        if username and password:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                raise serializers.ValidationError("Invalid username or password")

            if user.check_password(password):
                attrs["user"] = user
            else:
                raise serializers.ValidationError("Invalid username or password")
        else:
            raise serializers.ValidationError("Username and password are required")

        return attrs


class UserLogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()


class IbsTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user, *args, **kwargs):
        token = super().get_token(user)

        token["user_id"] = user.id
        token["username"] = user.username
        token["email"] = user.email
        token["groups"] = [group.id for group in user.groups.all()]
        token["branch"] = user.branch.id if user.branch else None

        return token


class ChangePasswordSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    confirm_password = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            "old_password",
            "new_password",
            "confirm_password",
        ]
