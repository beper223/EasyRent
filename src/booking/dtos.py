from datetime import timedelta, date
from rest_framework.serializers import ModelSerializer, ValidationError

from src.booking.models import Booking
from src.choices import BookingStatus

class BookingBaseDTO(ModelSerializer):
    """Unified serializer for creating and updating bookings
    (При создании: проверяем даты, пересечения и ставим статус pending.
    После создания: можно менять только статус, по правилам переходов.)
    """
    class Meta:
        model = Booking
        fields = [
            "id",
            "listing",
            "tenant",
            "start_date",
            "end_date",
            "status",
            "cancellable_until",
        ]
        read_only_fields = ["tenant", "cancellable_until"]

class BookingCreateDTO(BookingBaseDTO):
    """Unified serializer for creating and updating bookings"""

    def validate(self, attrs):
        user = self.context["request"].user
        instance = getattr(self, "instance", None)
        new_status = attrs.get("status", BookingStatus.PENDING)

        # ----------------------
        # Создание бронирования
        # ----------------------
        start_date = attrs.get("start_date")
        end_date = attrs.get("end_date")
        listing = attrs.get("listing")

        # 1. Дата окончания должна быть позже даты начала
        if start_date > end_date:
            raise ValidationError("End date cannot be earlier than start date.")

        # 2. Проверка пересечений с другими активными бронированиями
        overlapping = Booking.objects.filter(
            listing=listing,
            status__in=[BookingStatus.PENDING, BookingStatus.CONFIRMED, BookingStatus.CHECKED],
            start_date__lt=end_date,  # начало раньше конца нового
            end_date__gt=start_date  # окончание позже начала нового
        )
        if overlapping.exists():
            raise ValidationError("This listing is already booked for the selected dates.")

        # Статус всегда pending
        if "status" in attrs and new_status != BookingStatus.PENDING:
            raise ValidationError("New bookings must always start with status 'pending'.")

        return attrs

    def create(self, validated_data):
        # При создании автоматически устанавливаем cancellable_until
        start_date = validated_data["start_date"]
        listing = validated_data["listing"]
        validated_data["cancellable_until"] = start_date - timedelta(days=listing.cancellation_deadline_days)
        validated_data["status"] = BookingStatus.PENDING
        validated_data["tenant"] = self.context["request"].user
        return super().create(validated_data)

class BookingUpdateDTO(BookingBaseDTO):
    """Unified serializer for updating bookings"""

    class Meta(BookingBaseDTO.Meta):
        read_only_fields = BookingBaseDTO.Meta.read_only_fields + [
            "listing", "start_date", "end_date"
        ]
    def validate(self, attrs):
        user = self.context["request"].user
        instance = self.instance
        new_status = attrs.get("status", BookingStatus.PENDING)

        non_status_fields = set(attrs.keys()) - {"status"}
        if non_status_fields:
            raise ValidationError(
                f"Cannot update fields {', '.join(non_status_fields)}; only 'status' can be changed."
            )

        current = instance.status

        # --- transitions ---
        if current == BookingStatus.PENDING:
            if new_status == BookingStatus.CONFIRMED:
                if not (hasattr(user, "profile") and user.profile.role == "landlord"):
                    raise ValidationError("Only landlord can confirm a pending booking.")
            elif new_status == BookingStatus.REJECTED:
                if not (hasattr(user, "profile") and user.profile.role == "landlord"):
                    raise ValidationError("Only landlord can reject a pending booking.")
            elif new_status == BookingStatus.CANCELLED:
                if not (hasattr(user, "profile") and user.profile.role == "tenant"):
                    raise ValidationError("Only tenant can cancel a pending booking.")
            else:
                raise ValidationError("Invalid status change from 'pending'.")

        elif current == BookingStatus.CONFIRMED:
            if new_status == BookingStatus.CANCELLED:
                if not (hasattr(user, "profile") and user.profile.role == "tenant"):
                    raise ValidationError("Only tenant can cancel a confirmed booking.")
                if date.today() > instance.cancellable_until:
                    raise ValidationError("Cancellation period has expired for this booking.")
            elif new_status == BookingStatus.CHECKED:
                if not (hasattr(user, "profile") and user.profile.role == "landlord"):
                    raise ValidationError("Only landlord can mark confirmed booking as checked.")
                if date.today() < instance.start_date:
                    raise ValidationError(
                        f"Booking cannot be marked as checked before its start date ({instance.start_date})."
                    )
            else:
                raise ValidationError("Invalid status change from 'confirmed'.")

        else:
            raise ValidationError(f"Cannot change status from '{current}'.")

        return attrs

