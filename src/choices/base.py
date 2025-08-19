from django.db import models


class UserRole(models.TextChoices):
    TENANT = "tenant", "Арендатор"
    LANDLORD = "landlord", "Арендодатель"
    ADMIN = "administrator", "Администратор"

class HousingType(models.TextChoices):
    APARTMENT = "apartment", "Квартира"
    HOUSE = "house", "Дом"
    STUDIO = "studio", "Студия"
    ROOM = "room", "Комната"

class BookingStatus(models.TextChoices):
    PENDING = "pending", "Ожидает подтверждения"
    CONFIRMED = "confirmed", "Подтверждено"
    REJECTED = "rejected", "Отклонено"
    CANCELLED = "cancelled", "Отменено"
