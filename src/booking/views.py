from datetime import timedelta

from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from src.booking.models import Booking
from src.booking.dtos import BookingBaseDTO, BookingCreateDTO, BookingUpdateDTO
from src.permissions import IsTenantOrLandlordOrAdmin


class BookingViewSet(ModelViewSet):
    """
    ViewSet для управления бронированиями.
    Позволяет создавать, просматривать, обновлять и отменять бронирования.
    
    ViewSet zur Verwaltung von Buchungen.
    Ermöglicht das Erstellen, Anzeigen, Aktualisieren und Stornieren von Buchungen.
    
    Права доступа:
    - Арендаторы: могут управлять своими бронированиями
    - Арендодатели: могут управлять бронированиями своих объявлений
    - Администраторы: полный доступ
    
    Zugriffsrechte:
    - Mieter: können eigene Buchungen verwalten
    - Vermieter: können Buchungen für ihre Anzeigen verwalten
    - Administratoren: Vollzugriff
    """
    queryset = Booking.objects.all()
    permission_classes = [IsAuthenticated, IsTenantOrLandlordOrAdmin]

    def get_serializer_class(self):
        """
        Возвращает соответствующий сериализатор в зависимости от действия.
        - Создание: BookingCreateDTO
        - Обновление: BookingUpdateDTO
        - Остальные действия: BookingBaseDTO
        
        Gibt den entsprechenden Serializer basierend auf der Aktion zurück.
        - Erstellen: BookingCreateDTO
        - Aktualisieren: BookingUpdateDTO
        - Andere Aktionen: BookingBaseDTO
        """
        if self.action == "create":
            return BookingCreateDTO
        if self.action in ["update", "partial_update"]:
            return BookingUpdateDTO
        return BookingBaseDTO

    def perform_create(self, serializer):
        """
        Создает новое бронирование.
        Устанавливает арендатора и рассчитывает дату, до которой можно отменить бронирование.
        
        Erstellt eine neue Buchung.
        Setzt den Mieter und berechnet das Datum, bis zu dem die Stornierung möglich ist.
        """
        listing = serializer.validated_data["listing"]
        start_date = serializer.validated_data["start_date"]
        # вычисляем дату, до которой можно отменить
        cancellable_until = start_date - timedelta(days=listing.cancellation_deadline_days)

        serializer.save(
            tenant=self.request.user,
            cancellable_until=cancellable_until
        )

    def get_queryset(self):
        """
        Возвращает queryset бронирований в зависимости от прав пользователя.
        - Администраторы: все бронирования
        - Арендодатели: бронирования своих объявлений
        - Арендаторы: только свои бронирования
        
        Gibt einen QuerySet von Buchungen zurück, abhängig von den Benutzerrechten.
        - Administratoren: alle Buchungen
        - Vermieter: Buchungen für ihre Anzeigen
        - Mieter: nur eigene Buchungen
        """
        user = self.request.user

        if user.is_staff:
            # администратор видит все бронирования
            return Booking.objects.all()

        if hasattr(user, "profile") and user.profile.role == "landlord":
            # арендодатель видит бронирования своих Listing
            return Booking.objects.filter(listing__landlord=user)

        # tenant видит только свои бронирования
        return Booking.objects.filter(tenant=user)
