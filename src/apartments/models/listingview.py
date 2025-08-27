from django.db import models
from django.contrib.auth.models import User
from src.apartments.models.listing import Listing

class ListingView(models.Model):
    """
    Модель для учета просмотров объявлений.
    Хранит количество просмотров для каждого пользователя/IP.
    """
    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE, 
        related_name="views",
        verbose_name="Listing"
    )
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="listing_views",
        null=True,  # Для анонимных пользователей
        blank=True,
        verbose_name="User"
    )
    ip_address = models.GenericIPAddressField(
        null=True, 
        blank=True,
        verbose_name="IP Address"
    )
    view_count = models.PositiveIntegerField(
        default=1,
        verbose_name="View Count"
    )
    
    class Meta:
        verbose_name = "Listing View"
        verbose_name_plural = "Listing Views"
        unique_together = ("listing", "user", "ip_address")
        
    def __str__(self):
        viewer = self.user.username if self.user else self.ip_address
        return f"{viewer} - {self.listing} (просмотров: {self.view_count})"