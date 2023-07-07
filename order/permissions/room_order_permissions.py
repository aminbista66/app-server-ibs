from rest_framework.permissions import BasePermission


class CanViewRoomOrderPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and request.user.has_perm('order.view_roomorder')
        )

class CanChangeRoomOrderPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and request.user.has_perm('order.change_roomorder')
        )

class CanCreateRoomOrderPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and request.user.has_perm('order.create_roomorder')
        )

class CanDeleteRoomOrderPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and request.user.has_perm('order.delete_roomorder')
        )