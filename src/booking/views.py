from datetime import timedelta

from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from src.booking.models import Booking
from src.booking.dtos import BookingDTO
from src.permissions import IsTenantOrLandlordOrAdmin


class BookingViewSet(ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingDTO
    permission_classes = [IsAuthenticated, IsTenantOrLandlordOrAdmin]

    def perform_create(self, serializer):
        listing = serializer.validated_data["listing"]
        start_date = serializer.validated_data["start_date"]
        # вычисляем дату, до которой можно отменить
        cancellable_until = start_date - timedelta(days=listing.cancellation_deadline_days)

        serializer.save(
            tenant=self.request.user,
            cancellable_until=cancellable_until
        )
