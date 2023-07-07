from django.urls import path

from .views import (
    TaxRuleListAPIView,
    TaxRuleCreateAPIView,
    TaxRuleRetrieveUpdateDeleteAPIView,
    DiscountRuleListAPIView,
    DiscountRuleCreateAPIView,
    DiscountRuleRetrieveUpdateDeleteAPIView,
)

urlpatterns = [
    path("taxrules/", TaxRuleListAPIView.as_view(), name="taxrule-list"),
    path("taxrules/create/", TaxRuleCreateAPIView.as_view(), name="taxrule-create"),
    path(
        "taxrules/<int:pk>/",
        TaxRuleRetrieveUpdateDeleteAPIView.as_view(),
        name="taxrule-retrieve-update-delete",
    ),
    path(
        "discountrules/",
        DiscountRuleListAPIView.as_view(),
        name="discountrule-list",
    ),
    path(
        "discountrules/create/",
        DiscountRuleCreateAPIView.as_view(),
        name="discoutrule-create",
    ),
    path(
        "discountrules/<int:pk>/",
        DiscountRuleRetrieveUpdateDeleteAPIView.as_view(),
        name="discountrule-retrieve-update-delete",
    ),
]
