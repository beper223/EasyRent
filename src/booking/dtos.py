from datetime import timedelta

from rest_framework.serializers import ModelSerializer, ValidationError

from src.booking.models import Booking


class BookingDTO(ModelSerializer):
    class Meta:
        model = Booking
        fields = [
            "id",
            "listing",
            "tenant",
            "start_date",
            "end_date",
            "status",
            "cancellable_until"
        ]

    def validate(self, attrs):
        """
        Проверяем, что:
        1. Дата окончания позже даты начала.
        2. Нет пересечения с другими активными бронированиями.
        """
        start_date = attrs.get("start_date")
        end_date = attrs.get("end_date")
        listing = attrs.get("listing")

        if start_date > end_date:
            raise ValidationError("Дата окончания бронирования не быть меньше даты начала.")

        # проверка пересечений
        overlapping = Booking.objects.filter(
            listing=listing,
            status__in=["pending", "confirmed", "checked"],  # только активные
            start_date__lt=end_date,  # начало раньше окончания нового
            end_date__gt=start_date  # окончание позже начала нового
        )
        if overlapping.exists():
            raise ValidationError("Данное жильё уже забронировано на выбранные даты.")

        return attrs