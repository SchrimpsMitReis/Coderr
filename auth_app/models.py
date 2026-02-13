from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """
    Erweiterungsprofil zum Django `User`.

    Zweck:
    - Trennt Auth-Daten (User: username/password) von Profildaten.
    - Speichert den Profiltyp (Customer/Business) für Permissions/Business-Logik.
    - Enthält optionale Stammdaten (Name, Telefon, Standort, Beschreibung, Arbeitszeiten).

    Hinweis:
    - `user` ist OneToOne -> genau ein Profil pro User.
    - `type` wird typischerweise bei Registration gesetzt und später für Berechtigungen genutzt.
    """

    class UserType(models.TextChoices):
        """Erlaubte Rollen/Profiltypen im System."""
        CUSTOMER = "customer", "Customer"
        BUSINESS = "business", "Business"
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField()
    type = models.CharField(max_length=8, choices=UserType.choices)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    file = models.CharField(max_length=80, blank=True)
    location = models.CharField(max_length=80, blank=True)
    tel = models.CharField(max_length=30, blank=True)
    description = models.TextField(blank=True)
    working_hours = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Hilfreich im Django Admin und beim Debugging."""
        return f"{self.user.username} ({self.type})"