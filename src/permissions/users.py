from rest_framework import permissions
from rest_framework.request import Request


class IsAdminOrSelf(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return obj == request.user

class IsAnonymous(permissions.BasePermission):
    def has_permission(self, request: Request, view):
        return not request.user.is_authenticated
