from django.urls import path
from inventory.views.inventory_views import (
    InventoryCreateAPIView,
    InventoryListAPIView,
    InventoryRetrieveDeleteAPIView,
)
from inventory.views.inventory_category_views import (
    InventoryCategoryCreateAPIView,
    InventoryCategoryListAPIView,
    InventoryCategoryRetrieveUpdateDeleteAPIView,
)
from inventory.views.inventory_item_views import (
    InventoryItemCreateAPIView,
    InventoryItemListAPIView,
    InventoryItemRetrieveUpdateDeleteAPIView,
)

from inventory.views.measurement_unit_views import (
    MeasurementUnitCreateAPIView,
    MeasurementUnitListAPIView,
    MeasurementUnitRetrieveUpdateDeleteAPIView,
)
from inventory.views.send_to_sub_store_views import SendToSubStoreAPIView
from inventory.views.sub_store_views import (
    SubStoreCreateAPIView,
    SubStoreListAPIView,
    SubStoreRetrieveUpdateDeleteAPIView,
)

urlpatterns = [
    path(
        "measurementunits/",
        MeasurementUnitListAPIView.as_view(),
        name="measurementunit-list",
    ),
    path(
        "measurementunits/create/",
        MeasurementUnitCreateAPIView.as_view(),
        name="measurementunit-create",
    ),
    path(
        "measurementunits/<int:pk>/",
        MeasurementUnitRetrieveUpdateDeleteAPIView.as_view(),
        name="measurementunit-retrieve-update-delete",
    ),
    path(
        "categories/",
        InventoryCategoryListAPIView.as_view(),
        name="inventorycategory-list",
    ),
    path(
        "categories/create/",
        InventoryCategoryCreateAPIView.as_view(),
        name="inventorycategory-create",
    ),
    path(
        "categories/<int:pk>/",
        InventoryCategoryRetrieveUpdateDeleteAPIView.as_view(),
        name="inventorycategory-retrieve-update-delete",
    ),
    path(
        "items/",
        InventoryItemListAPIView.as_view(),
        name="inventoryitem-list",
    ),
    path(
        "items/create/",
        InventoryItemCreateAPIView.as_view(),
        name="inventoryitem-create",
    ),
    path(
        "items/<int:pk>/",
        InventoryItemRetrieveUpdateDeleteAPIView.as_view(),
        name="inventoryitem-retrieve-update-delete",
    ),
    path(
        "substores/",
        SubStoreListAPIView.as_view(),
        name="substore-list",
    ),
    path(
        "substores/create/",
        SubStoreCreateAPIView.as_view(),
        name="substore-create",
    ),
    path(
        "substores/<pk>/",
        SubStoreRetrieveUpdateDeleteAPIView.as_view(),
        name="substore-retrieve-update-delete",
    ),
    path("", InventoryListAPIView.as_view(), name="inventory-list"),
    path(
        "<int:pk>/",
        InventoryRetrieveDeleteAPIView.as_view(),
        name="inventory-retrieve-delete",
    ),
    path(
        "sendtosubstore/",
        SendToSubStoreAPIView.as_view(),
        name="send-to-sub-store",
    ),
]
