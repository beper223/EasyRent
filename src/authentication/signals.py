from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from src.authentication.models import Profile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Автоматически создаём профиль при регистрации пользователя"""
    if created:
        Profile.objects.create(user=instance) #role=UserRole.TENANT


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Сохраняем профиль при сохранении пользователя"""
    instance.profile.save()