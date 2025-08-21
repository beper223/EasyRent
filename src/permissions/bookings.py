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

    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated:
            return False

        # Admin имеет полный доступ / Administrator hat vollen Zugriff
        if user.is_staff:
            return True

        # Создание (POST) доступно только tenant / Erstellung (POST) ist nur für Tenant verfügbar
        if view.action == "create":
            return hasattr(user, "profile") and user.profile.role == "tenant"

        # Для остальных действий пока пускаем, но проверим в has_object_permission
        # Für andere Aktionen lassen wir es vorerst zu, aber prüfen es in has_object_permission
        return True

    def has_object_permission(self, request, view, obj):
        user = request.user

        if user.is_staff:
            return True  # админ видит всё / Administrator sieht alles

        if hasattr(user, "profile"):
            if user.profile.role == "tenant":
                return obj.tenant == user  # tenant видит только свои / Tenant sieht nur seine eigenen
            if user.profile.role == "landlord":
                return obj.listing.landlord == user  # landlord видит свои listing / Vermieter sieht nur seine Listings
        return False