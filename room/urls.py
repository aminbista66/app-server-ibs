from django.urls import path

from .views import (
    RoomCategoryCreateAPIView,
    RoomCategoryListAPIView,
    RoomCategoryRetrieveUpdateDeleteAPIView,
    RoomListAPIView,
    RoomCreateAPIView,
    RoomRetrieveUpdateDeleteAPIView,
    RoomFeatureListAPIView,
    RoomFeatureCreateAPIView,
    RoomFeatureRetrieveUpdateDeleteAPIView,
    BookedRoomListAPIView,
    BookedRoomCreateAPIView,
    BookedRoomRetrieveUpdateDeleteAPIView
)


urlpatterns = [
    path("", RoomListAPIView.as_view(), name="room-list"),
    path("create/", RoomCreateAPIView.as_view(), name="room-create"),
    path(
        "<int:pk>/",
        RoomRetrieveUpdateDeleteAPIView.as_view(),
        name="room-retrieve-update-delete",
    ),
    # room categories urls
    path("categories/", RoomCategoryListAPIView.as_view(), name="roomcategory-list"),
    path(
        "categories/create/",
        RoomCategoryCreateAPIView.as_view(),
        name="roomcategory-create",
    ),
    path(
        "categories/<int:pk>/",
        RoomCategoryRetrieveUpdateDeleteAPIView.as_view(),
        name="roomcategory-retrieve-update-delete",
    ),
    # room features urls
    path("features/", RoomFeatureListAPIView.as_view(), name="roomfeatures-list"),
    path(
        "features/create/",
        RoomFeatureCreateAPIView.as_view(),
        name="roomfeatures-create",
    ),
    path(
        "features/<int:pk>/",
        RoomFeatureRetrieveUpdateDeleteAPIView.as_view(),
        name="roomfeatures-retrieve-update-delete",
    ),
    # room booking urls
    path(
        'booked/list/', BookedRoomListAPIView.as_view(), name="bookedroom-list"
    ),
    path(
        'book/', BookedRoomCreateAPIView.as_view(), name="bookedroom-create"
    ),
    path(
        'booked/<int:pk>/',
        BookedRoomRetrieveUpdateDeleteAPIView.as_view(),
        name="bookedroom-retrieve-update-delete"
    )
]
