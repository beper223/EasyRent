from django.db import models
from django.contrib.auth.models import User
from src.apartments.models.listing import Listing

class ListingView(models.Model):
    """Уникальный просмотр объявления"""
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="views")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listing_views")
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("listing", "user")