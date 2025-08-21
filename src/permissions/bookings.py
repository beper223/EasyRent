from rest_framework.permissions import BasePermission

class IsTenantOrLandlordOrAdmin(BasePermission):
    """
    Разрешение:
    - tenant может работать только со своими бронированиями
    - landlord — со своими Listing
    - admin — со всеми

    Berechtigung:
    - Mieter kann nur mit seinen eigenen Buchungen arbeiten
    - Vermieter kann nur mit Buchungen seiner eigenen Listings arbeiten
    - Administrator kann alles sehen
    """
    def has_object_permission(self, request, view, obj):
        user = request.user

        if user.is_staff:
            return True  # админ видит всё / Administrator sieht alles

        if hasattr(user, "profile") and user.profile.role == "landlord":
            # арендодатель видит Booking, принадлежащие его Listing
            # Vermieter sieht nur Buchungen, die zu seinen Listings gehören
            return obj.listing.landlord == user

        # tenant видит только свои Booking
        # Mieter sieht nur seine eigenen Buchungen
        return obj.tenant == user