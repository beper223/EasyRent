from rest_framework.permissions import BasePermission
from src.choices import UserRole

class IsTenant(BasePermission):
    """
    Разрешение только для tenant
    / Berechtigung nur für Mieter
    """

    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        role = getattr(request.user.profile, "role", None)
        return role == UserRole.TENANT
