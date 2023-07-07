from django.urls import path

from product.views.product_views import ProductCreateAPIView, ProductListAPIView, ProductRetrieveUpdateDeleteAPIView

from .views.product_category_views import (
    ProductCategoryListAPIView,
    ProductCategoryCreateAPIView,
    ProductCategoryRetrieveUpdateDeleteAPIView,
)
from .views.product_image_views import (
    ProductImageCreateAPIView,
    ProductImageRetrieveDeleteAPIView
)
urlpatterns = [
    path(
        "categories/",
        ProductCategoryListAPIView.as_view(),
        name="productcategory_list"
    ),
    path(
        "categories/create/",
        ProductCategoryCreateAPIView.as_view(),
        name="productcategory_create"
    ),
    path(
        "categories/<int:pk>/",
        ProductCategoryRetrieveUpdateDeleteAPIView.as_view(),
        name="productcategory_retrieve_update_delete"
    ),
    
    path(
        "products/images/<int:pk>/",
        ProductImageRetrieveDeleteAPIView.as_view(),
        name="productcategory_retrieve_update_delete"
    ),
    path(
        "products/images/create/",
        ProductImageCreateAPIView.as_view(),
        name="productcategory_retrieve_update_delete"
    ),

    path(
        "",
        ProductListAPIView.as_view(),
        name="product-list"
    ),
    path(
        "create/",
        ProductCreateAPIView.as_view(),
        name="product-create"
    ),
    path(
        "<int:pk>/",
        ProductRetrieveUpdateDeleteAPIView.as_view(),
        name="product-retrieve-update-delete"
    )
]
