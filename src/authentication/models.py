from django.db import models
from django.contrib.auth.models import User
from django.utils.functional import cached_property

from src.choices import UserRole


class Profile(models.Model):
    """Extended user profile with additional information and role-based access."""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name="Profile"
    )
    
    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        verbose_name="User role",
    )
    
    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"
        ordering = ['user__username']
    
    def __str__(self) -> str:
        """String representation of the profile."""
        return f"{self.user.username} ({self.get_role_display()})"
    
    @cached_property
    def is_landlord(self) -> bool:
        """Check if user has landlord role."""
        return self.role == UserRole.LANDLORD
    
    @cached_property
    def is_tenant(self) -> bool:
        """Check if user has tenant role."""
        return self.role == UserRole.TENANT

