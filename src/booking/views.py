from datetime import timedelta

from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from src.booking.models import Booking
from src.booking.dtos import BookingBaseDTO, BookingCreateDTO, BookingUpdateDTO
from src.permissions import IsTenantOrLandlordOrAdmin


class BookingViewSet(ModelViewSet):
    queryset = Booking.objects.all()
    permission_classes = [IsAuthenticated, IsTenantOrLandlordOrAdmin]

    def get_serializer_class(self):
        if self.action == "create":
            return BookingCreateDTO
        if self.action in ["update", "partial_update"]:
            return BookingUpdateDTO
        return BookingBaseDTO

    def perform_create(self, serializer):
        listing = serializer.validated_data["listing"]
        start_date = serializer.validated_data["start_date"]
        # вычисляем дату, до которой можно отменить
        cancellable_until = start_date - timedelta(days=listing.cancellation_deadline_days)

        serializer.save(
            tenant=self.request.user,
            cancellable_until=cancellable_until
        )

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            # администратор видит все бронирования
            return Booking.objects.all()

        if hasattr(user, "profile") and user.profile.role == "landlord":
            # арендодатель видит бронирования своих Listing
            return Booking.objects.filter(listing__landlord=user)

        # tenant видит только свои бронирования
        return Booking.objects.filter(tenant=user)
