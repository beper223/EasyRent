from django.db import models
from django.contrib.auth.models import User

from src.choices import UserRole


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        #default=UserRole.TENANT
    )

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"
