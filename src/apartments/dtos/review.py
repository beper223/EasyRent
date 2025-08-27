from rest_framework import serializers

from src.apartments.models import Review
from src.booking.models import Booking
from src.choices import BookingStatus


class ReviewCreateDTO(serializers.ModelSerializer):
    """
    Serializer for creating reviews.
    Serializer для создания отзывов.
    """
    listing = serializers.PrimaryKeyRelatedField(read_only=True)
    tenant = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = [
            "id",
            "listing",
            "tenant",
            "rating",
            "comment",
            "created_at"
        ]
        read_only_fields = ["tenant", "listing", "created_at"]

    def validate(self, attrs):
        request = self.context["request"]
        user = request.user
        listing = self.context["listing"]

        # Tenant-only check / Только арендаторы могут оставлять отзывы
        if not hasattr(user, "profile") or user.profile.role != "tenant":
            raise serializers.ValidationError("Only tenants can leave reviews.")

        # Booking must exist and be checked / Бронирование должно существовать и быть завершенным
        has_valid_booking = Booking.objects.filter(
            tenant=user,
            listing=listing,
            status=BookingStatus.CHECKED,
        ).exists()

        if not has_valid_booking:
            raise serializers.ValidationError(
                "You can only leave a review after a completed booking for this listing."
            )

        # Prevent multiple reviews / Запрет на несколько отзывов
        if Review.objects.filter(tenant=user, listing=listing).exists():
            raise serializers.ValidationError("You have already left a review for this listing.")

        return attrs

    def create(self, validated_data):
        validated_data["tenant"] = self.context["request"].user
        validated_data["listing"] = self.context["listing"]
        return super().create(validated_data)


class ReviewDTO(serializers.ModelSerializer):
    """
    Serializer for displaying reviews.
    Serializer для отображения отзывов.
    """
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    tenant = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True
    )

    class Meta:
        model = Review
        fields = [
            "id",
            "tenant",
            "rating",
            "comment",
            "created_at"
        ]

