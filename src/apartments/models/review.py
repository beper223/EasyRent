from django.db import models
from django.contrib.auth.models import User
from src.apartments.models.listing import Listing

class Review(models.Model):
    #booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name="review")
    tenant = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveSmallIntegerField(default=5)  # 1–5
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("tenant", "listing")  # один отзыв на одно объявление от арендатора

    def __str__(self):
        return f"Отзыв {self.tenant.name} → {self.listing.title} ({self.rating}★)"