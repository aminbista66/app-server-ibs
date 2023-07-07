from django.urls import path

from .views import ListActionLogApiView

urlpatterns = [
    path("", ListActionLogApiView.as_view(), name="list_log_action"),

]   