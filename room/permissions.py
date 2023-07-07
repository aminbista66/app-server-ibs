from rest_framework.permissions import BasePermission


class CanCreateRoomCategoryPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('room.add_roomcategory')
        )


class CanChangeRoomCategoryPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('room.change_roomcategory')
        )


class CanViewRoomCategoryPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('room.view_roomcategory')
        )


class CanDeleteRoomCategoryPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('room.delete_roomcategory')
        )


class CanCreateRoomFeaturePermission(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('room.add_roomfeature')
        )


class CanChangeRoomFeaturePermission(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('room.change_roomfeature')
        )


class CanViewRoomFeaturePermission(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('room.view_roomfeature')
        )


class CanDeleteRoomFeaturePermission(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('room.delete_roomfeature')
        )


class CanCreateRoomPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('room.add_room')
        )


class CanChangeRoomPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('room.change_room')
        )


class CanViewRoomPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('room.view_room')
        )


class CanDeleteRoomPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('room.delete_room')
        )


''' Room Booking CRUD Permissions '''


class CanCreateBookedRoomPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and request.user.has_perm(
                'room.create_bookedroom')
        )

class CanViewBookedRoomPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and request.user.has_perm(
                'room.view_bookedroom')
        )

class CanChangeBookedRoomPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and request.user.has_perm(
                'room.change_bookedroom')
        )
    
class CanDeleteBookedRoomPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and request.user.has_perm(
                'room.delete_bookedroom')
        )