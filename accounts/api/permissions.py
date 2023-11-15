from rest_framework.permissions import BasePermission


class IsSeekerUser(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        return bool(request.user and request.user.is_seeker)


class IsShelterUser(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        return bool(request.user and request.user.is_shelter)