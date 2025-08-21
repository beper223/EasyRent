from datetime import timedelta, date
from rest_framework.serializers import ModelSerializer, ValidationError

from src.booking.models import Booking
from src.choices import BookingStatus


class BookingDTO(ModelSerializer):
    """Unified serializer for creating and updating bookings"""

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
        read_only_fields = ["tenant", "listing", "start_date", "end_date", "cancellable_until"]

    def validate(self, attrs):
        user = self.context["request"].user
        instance = getattr(self, "instance", None)
        new_status = attrs.get("status", BookingStatus.PENDING)

        # Создание: статус всегда pending
        if not instance and new_status != BookingStatus.PENDING:
            raise ValidationError("New bookings must have status 'pending'.")

        # После создания: остальные поля менять нельзя
        if instance:
            non_status_fields = set(attrs.keys()) - {"status"}
            if non_status_fields:
                raise ValidationError(
                    f"Cannot update fields {', '.join(non_status_fields)}; only status can be changed."
                )

            current = instance.status

            # Проверка допустимых переходов статусов
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
                else:
                    raise ValidationError("Invalid status change from 'confirmed'.")

            else:
                raise ValidationError(f"Cannot change status from '{current}'.")

        return attrs

    def create(self, validated_data):
        # При создании автоматически устанавливаем cancellable_until
        start_date = validated_data["start_date"]
        listing = validated_data["listing"]
        validated_data["cancellable_until"] = start_date - timedelta(days=listing.cancellation_deadline_days)
        validated_data["status"] = BookingStatus.PENDING
        validated_data["tenant"] = self.context["request"].user
        return super().create(validated_data)