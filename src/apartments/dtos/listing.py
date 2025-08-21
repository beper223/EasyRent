from django.contrib.auth.models import User
from rest_framework import serializers

from src.apartments.models import Listing
from src.choices import HousingType

class LandlordDTO(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]

class ListingCompactDTO(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    class Meta:
        model = Listing
        fields = [
            "id",
            "title",
            "description",
            "location",
            "price",
            "rooms",
            "housing_type",
            "is_active",
            "created_at",
            "cancellation_deadline_days"
]

class ListingDTO(ListingCompactDTO):
    landlord = LandlordDTO(read_only=True)

    class Meta(ListingCompactDTO.Meta):
        fields = ListingCompactDTO.Meta.fields + ["landlord"]

    def to_representation(self, instance):
        """Показываем поле is_active только админу"""
        data = super().to_representation(instance)
        user = self.context.get("request").user

        if not user.is_staff:
            data.pop("is_active", None)

        return data
