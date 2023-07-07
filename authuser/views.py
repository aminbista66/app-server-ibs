import base64
from datetime import datetime
import json
import time
import geocoder

from django.contrib.auth.models import Group, Permission
from django.contrib.auth.hashers import check_password

from rest_framework.pagination import LimitOffsetPagination
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework import generics, status, serializers
from common.permissions import IsTenantAdminOrHasBranchAccessPermission
from ibs.exceptions import InternalServerError
from logs.logs_mixins import (
    CustomCreateAPIView,
    CustomDeleteAPIView,
    CustomRetrieveUpdateDeleteAPIView,
    CustomUpdateAPIView,
    get_client_ip,
)
from subscription.exceptions import (
    DeviceLimitReached,
    TenantDoesNotExist,
    SubscriptionDoesNotExist,
)
from subscription.models import DevicesHistory

from subscription.decorators import check_subscription_expiry
from .models import User
from .serializers import (
    CreateGroupSerializer,
    IbsTokenObtainPairSerializer,
    PermissionSerializer,
    UserCreateSerializer,
    GroupSerializer,
    UserLoginSerializer,
    ChangePasswordSerializer,
    UserLogoutSerializer,
    UserSerializer,
)
from .exceptions import RefreshTokenExpired, InvalidTokenType
from subscription.models import Subscription
from tenants.models import Tenant

from .permissions import (
    CanChangeUserPermission,
    CanCreateUserPermission,
    CanDeleteUserPermission,
    CanViewUserPermission,
    CanCreateGroupPermission,
    CanDeleteGroupPermission,
    CanViewGroupPermission,
    CanChangeGroupPermission,
)

from ibs.settings import env
from tenants.utils import hostname_from_request


USER_LIST_MESSAGE = ("User list retrieved succesfully",)
SUCCESS_LOGIN_MESSAGE = ("User logged in successfully",)
PASSWORD_CHANGED_MESSAGE = ("Password changed successfully",)
PASSWORD_INCORRECT_MESSAGE = ("Password is invalid",)
PASSWORD_DONOT_MATCHED_MESSAGE = ("Password and confirm password do not match",)
GROUP_RETRIEVE_MESSAGE = ("Group retrieved successfully",)


class LoginView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    @check_subscription_expiry
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]

        subdomain = hostname_from_request(request)

        try:
            tenant = Tenant.objects.using("default").get(subdomain=subdomain)
            try:
                subscription = Subscription.objects.using("default").get(tenant=tenant)

                if subscription.is_device_limit_reached():
                    raise DeviceLimitReached()

                subscription.device_count += 1
                subscription.save(using="default")

                refresh = IbsTokenObtainPairSerializer.get_token(user)

                user_ip = geocoder.ip(str(get_client_ip(request)))

                device_history = DevicesHistory()
                device_history.device_ip = get_client_ip(request)
                device_history.device_type = request.user_agent.device.family
                device_history.location = (
                    f"{user_ip.city}, {user_ip.state}, {user_ip.country}"
                )
                device_history.device_os = f"{request.user_agent.os.family}/{request.user_agent.os.version_string}"
                device_history.browser_type = f"{request.user_agent.browser.family}/{request.user_agent.browser.version_string}"
                device_history.device_user = tenant.name
                device_history.subscription = subscription
                device_history.refresh_token = str(refresh)
                device_history.is_active = 1
                device_history.last_login = datetime.now()
                device_history.save(using="default")

                return Response(
                    {
                        "message": SUCCESS_LOGIN_MESSAGE,
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    }
                )
            except Subscription.DoesNotExist:
                raise SubscriptionDoesNotExist()
        except Tenant.DoesNotExist:
            raise TenantDoesNotExist()


class LogoutAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserLogoutSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        refresh_token = serializer.validated_data["refresh_token"]
        jwt_bytest_decoded = json.loads(
            (
                base64.b64decode(
                    refresh_token.split(".")[1].encode("ascii")
                    + b"=" * (-len(refresh_token.split(".")[1].encode("ascii")) % 4)
                )
            ).decode("ascii")
        )
        exp = jwt_bytest_decoded["exp"]
        time_expired_check = exp - time.time()
        """
        Check the expired time
        """
        if time_expired_check <= 0:
            raise RefreshTokenExpired()
        """
        check if token is refresh or not
        """
        if jwt_bytest_decoded["token_type"] != "refresh":
            return InvalidTokenType()

        token = RefreshToken(refresh_token)
        token.blacklist()

        subdomain = hostname_from_request(request)
        try:
            tenant = Tenant.objects.using("default").get(subdomain=subdomain)
            subcription = Subscription.objects.using("default").get(tenant=tenant.id)
            if subcription.device_count > 0:
                subcription.device_count -= 1
                subcription.save(using="default")

            DevicesHistory.objects.using("default").filter(
                refresh_token=refresh_token
            ).update(is_active=0)

            return Response(
                {"message": "User logout successfully"}, status=status.HTTP_200_OK
            )
        except:
            raise InternalServerError()


class ListUserApiView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [CanViewUserPermission]
    pagination_class = LimitOffsetPagination
    filter_backends = [SearchFilter]
    search_fields = ["email", "first_name", "last_name", "username"]

    def get_queryset(self):
        user = self.request.user
        return User.objects.get_user_of_self_branch(user)


class UserDetailUpdateDestroyAPIView(CustomRetrieveUpdateDeleteAPIView):
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [CanViewUserPermission()]
        elif self.request.method == "DELETE":
            return [CanDeleteUserPermission()]
        elif self.request.method == "PUT" or self.request.method == "PATCH":
            return [CanChangeUserPermission()]
        else:
            super().get_permissions()

    def get_queryset(self):
        user = self.request.user
        return User.objects.get_user_of_self_branch(user)


class CreateUserApiView(CustomCreateAPIView):
    serializer_class = UserCreateSerializer
    permission_classes = [CanCreateUserPermission]

    def get_queryset(self):
        user = self.request.user
        return User.objects.get_user_of_self_branch(user)


# thia ia api to change password.
class UserChangePasswordView(generics.UpdateAPIView):
    permission_classes = [CanChangeUserPermission]
    serializer_class = ChangePasswordSerializer

    def get_queryset(self):
        user = self.request.user
        return User.objects.get_user_of_self_branch(user)

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = self.get_object()

        old_password = serializer.validated_data["old_password"]
        new_password = serializer.validated_data["new_password"]
        confirm_password = serializer.validated_data["confirm_password"]

        if not check_password(old_password, user.password):
            raise serializers.ValidationError(detail=PASSWORD_INCORRECT_MESSAGE)

        if new_password != confirm_password:
            raise serializers.ValidationError(detail=PASSWORD_DONOT_MATCHED_MESSAGE)

        user.set_password(new_password)
        user.save()

        return Response(
            {"message": PASSWORD_CHANGED_MESSAGE}, status=status.HTTP_200_OK
        )


class ListPermissionApiView(generics.ListAPIView):
    http_method_names = ["get"]
    serializer_class = PermissionSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        subdomain = hostname_from_request(request)
        subscription = Subscription.objects.using("default").get(domain=subdomain)
        group = Group.objects.using("default").get(id=subscription.group_id)
        permissions = Permission.objects.using("default").filter(group=group)
        page = self.paginate_queryset(permissions)
        assert page is not None
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)


# group api
class UserGroupListAPIView(generics.ListAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [CanViewGroupPermission]


class UserGroupRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [CanViewGroupPermission]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(
            {"message": GROUP_RETRIEVE_MESSAGE, "result": serializer.data},
            status=status.HTTP_200_OK,
        )


class UserGroupDestroyAPIView(CustomDeleteAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [CanDeleteGroupPermission]


class UserGroupUpdateAPIView(CustomUpdateAPIView):
    queryset = Group.objects.all()
    serializer_class = CreateGroupSerializer
    permission_classes = [CanChangeGroupPermission]


class UserGroupCreateAPIView(CustomCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = CreateGroupSerializer
    permission_classes = [CanCreateGroupPermission]
