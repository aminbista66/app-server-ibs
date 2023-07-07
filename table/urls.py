from django.urls import path
from .views import (
    TableCategoryListAPIView,
    TableCategoryCreateAPIView,
    TableCategoryRetrieveUpdateDeleteAPIView,
    TableListAPIView,
    TableCreateAPIView,
    TableRetrieveUpdateDeleteAPIView,
)

urlpatterns = [
    path(
        "",
        TableListAPIView.as_view(),
        name="table-list",
    ),
    path(
        "create/",
        TableCreateAPIView.as_view(),
        name="table-create",
    ),
    path(
        "<int:pk>/",
        TableRetrieveUpdateDeleteAPIView.as_view(),
        name="table-retrieve-update-delete",
    ),
    path(
        "categories/",
        TableCategoryListAPIView.as_view(),
        name="table-list",
    ),
    path(
        "categories/create/",
        TableCategoryCreateAPIView.as_view(),
        name="table-create",
    ),
    path(
        "categories/<int:pk>/",
        TableCategoryRetrieveUpdateDeleteAPIView.as_view(),
        name="table-retrieve-update-delete",
    ),
]
