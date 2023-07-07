from rest_framework import generics
from common.permissions import IsTenantAdminOrHasBranchAccessPermission
from logs.logs_mixins import CustomCreateAPIView, CustomRetrieveUpdateDeleteAPIView
from product.filters.product_filters import ProductFilter
from product.models.product import Product
from product.permissions.ingredient_permissions import (
    CanCreateProductIngredientPermission,
    CanViewProductIngredientPermission,
    CanChangeProductIngredientPermission,
    CanDeleteProductIngredientPermission,
)
from product.permissions.product_permissions import (
    CanCreateProductPermission,
    CanViewProductPermission,
    CanChangeProductPermission,
    CanDeleteProductPermission,
)
from product.serializers.product_serializers import (
    ProductCreateSerializer,
    ProductSerializer,
)


class ProductListAPIView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [CanViewProductPermission, CanViewProductIngredientPermission]
    filterset_class = ProductFilter

    def get_queryset(self):
        branch = self.request.query_params.get("branch", None)
        fiscal_year = self.request.query_params.get("fiscal_year", None)
        return Product.objects.get_product_of_branch(branch, fiscal_year).order_by(
            "-created_at"
        )


class ProductCreateAPIView(CustomCreateAPIView):
    serializer_class = ProductCreateSerializer
    permission_classes = [
        IsTenantAdminOrHasBranchAccessPermission,
        CanCreateProductPermission,
        CanCreateProductIngredientPermission,
    ]

    def get_queryset(self):
        branch = self.request.query_params.get("branch", None)
        fiscal_year = self.request.query_params.get("fiscal_year", None)
        return Product.objects.get_product_of_branch(branch, fiscal_year)


class ProductRetrieveUpdateDeleteAPIView(CustomRetrieveUpdateDeleteAPIView):
    def get_serializer_class(self):
        method = self.request.method
        if method == "GET" or method == "DELETE":
            return ProductSerializer
        else:
            return ProductCreateSerializer

    def get_permissions(self):
        method = self.request.method

        if method == "GET":
            return [
                IsTenantAdminOrHasBranchAccessPermission(),
                CanViewProductPermission(),
                CanViewProductIngredientPermission(),
            ]
        elif method == "PUT" or method == "PATCH":
            return [
                IsTenantAdminOrHasBranchAccessPermission(),
                CanChangeProductIngredientPermission(),
                CanChangeProductPermission(),
            ]
        elif method == "DELETE":
            return [
                IsTenantAdminOrHasBranchAccessPermission(),
                CanDeleteProductIngredientPermission(),
                CanDeleteProductPermission(),
            ]
        else:
            return super().get_permissions()

    def get_queryset(self):
        branch = self.request.query_params.get("branch", None)
        fiscal_year = self.request.query_params.get("fiscal_year", None)
        return Product.objects.get_product_of_branch(branch, fiscal_year)
