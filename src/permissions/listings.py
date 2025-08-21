from rest_framework.permissions import BasePermission, SAFE_METHODS
from src.choices import UserRole


class IsLandlordOrAdmin(BasePermission):
    """
    Доступ на запись только арендодателям и администраторам.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True  # просмотр доступен всем
        # админ может всё
        if request.user.is_staff:
            return True
        if not request.user.is_authenticated:
            return False
        role = getattr(request.user.profile, "role", None)
        return role == UserRole.LANDLORD

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        # админ может всё
        if request.user.is_staff:
            return True
        # арендодатель может редактировать только свои объявления
        return obj.landlord == request.user