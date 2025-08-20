from django.contrib.auth.models import User
from rest_framework import serializers

from src.apartments.models import Listing


class LandlordDTO(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]

class ListingDTO(serializers.ModelSerializer):
    landlord = LandlordDTO(read_only=True)

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
            "landlord"
        ]
