from django.db import models


class UserRole(models.TextChoices):
    TENANT = "tenant", "Mieter"  # Der Mieter (mietet eine Unterkunft)
    LANDLORD = "landlord", "Vermieter"  # Der Vermieter (vermietet eine Unterkunft)
    ADMIN = "administrator", "Administrator"  # Der Administrator (Systemverwaltung)

class HousingType(models.TextChoices):
    APARTMENT = "apartment","Wohnung"  # Eine Wohnung (Квартира)
    HOUSE = "house",        "Haus"  # Ein Haus (Дом)
    STUDIO = "studio",      "Studio"  # Ein Studio / Einzimmerwohnung (Студия)
    ROOM = "room",          "Zimmer"  # Ein Zimmer (Комната)

class BookingStatus(models.TextChoices):
    PENDING = "pending",        "Ausstehend"  # Wartet auf Bestätigung durch den Vermieter
    CONFIRMED = "confirmed",    "Bestätigt"  # Vom Vermieter bestätigt
    REJECTED = "rejected",      "Abgelehnt"  # Vom Vermieter abgelehnt
    CANCELLED = "cancelled",    "Storniert"  # Vom Mieter storniert
    CHECKED = "checked",        "Abgeschlossen"  # Aufenthalt beendet, bestätigt
