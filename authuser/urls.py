from .views import (
    ListUserApiView,
    UserChangePasswordView,
    CreateUserApiView,
    ListPermissionApiView,
    UserDetailUpdateDestroyAPIView,
    UserGroupCreateAPIView,
    UserGroupUpdateAPIView,
    UserGroupRetrieveAPIView,
    UserGroupDestroyAPIView,
    UserGroupListAPIView,
    LoginView,
    LogoutAPIView,
)
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path, include

router = routers.DefaultRouter()

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("login/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
    
    path(
        "changepassword/<int:pk>/",
        UserChangePasswordView.as_view(),
        name="change-password",
    ),
    path("register/", CreateUserApiView.as_view(), name="register-user"),
    path("users/", ListUserApiView.as_view(), name="user-list"),
    path("users/<int:pk>/", UserDetailUpdateDestroyAPIView.as_view(), name="user-detail-update-destroy"),
    
    path("permissions/", ListPermissionApiView.as_view(), name="auth-permissions"),
    
    path("groups/", UserGroupListAPIView.as_view(), name="auth-groups-list"),
    path("groups/create/", UserGroupCreateAPIView.as_view(), name="auth-groups-create"),
    path(
        "groups/<int:pk>/",
        UserGroupRetrieveAPIView.as_view(),
        name="auth-groups-retrieve",
    ),
    path(
        "groups/update/<int:pk>/",
        UserGroupUpdateAPIView.as_view(),
        name="auth-groups-update",
    ),
    path(
        "groups/delete/<int:pk>/",
        UserGroupDestroyAPIView.as_view(),
        name="auth-groups-destroy",
    ),
]

urlpatterns = urlpatterns + router.urls
