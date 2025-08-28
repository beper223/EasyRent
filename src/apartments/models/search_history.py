from django.db import models
from django.contrib.auth.models import User

class SearchHistory(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="search_history",
        null=True,  # Для анонимных пользователей
        blank=True,
        verbose_name="User"
    )
    keyword = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    search_count = models.PositiveIntegerField(
        default=1,
        verbose_name="Search Count"
    )
    class Meta:
        verbose_name = "Search View"
        verbose_name_plural = "Search Views"
        unique_together = ("keyword", "user")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} → {self.keyword}"