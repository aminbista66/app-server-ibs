from django.urls import path
from .views import (
    FiscalYearListAPIView,
    # FiscalYearCreateAPIView,
    # FiscalYearRetrieveUpdateDeleteAPIView,
)


urlpatterns = [
    path(
        "",
        FiscalYearListAPIView.as_view(),
        name="fiscalyear-list"
    ),
    # path("create/", FiscalYearCreateAPIView.as_view(), name="fiscalyear-create"),
    # path("<pk>/", FiscalYearRetrieveUpdateDeleteAPIView.as_view(), name="fiscalyear-retrieve-update-delete")
]
