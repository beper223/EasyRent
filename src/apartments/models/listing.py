from django.db import models
from django.contrib.auth.models import User

from src.choices import HousingType

class Listing(models.Model):
    landlord = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    rooms = models.PositiveIntegerField()
    housing_type = models.CharField(max_length=20, choices=HousingType.choices)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.price}"
