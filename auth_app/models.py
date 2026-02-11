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

    # 1:1 Verknüpfung zum Auth-User (Login-Daten liegen im User-Modell)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Kontakt-E-Mail für Profilzwecke (kann = User.email sein; bewusst doppelt, falls später getrennt)
    email = models.EmailField()

    # Profiltyp: steuert Berechtigungen (z.B. Customer darf X, Business darf Y)
    type = models.CharField(
        max_length=8,               # "customer" (8) / "business" (8)
        choices=UserType.choices,
        # optional sinnvoll:
        # default=UserType.CUSTOMER,
    )

    # Optional: Profildaten (nicht zwingend bei Registrierung)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)

    # Optional: Dateiname/Referenz zu einem Profilbild/Dokument (kein FileField)
    file = models.CharField(max_length=80, blank=True)

    # Optional: Freitext-Standort (z.B. Stadt), nicht zwingend Geo-Koordinaten
    location = models.CharField(max_length=80, blank=True)

    # Optional: Telefonnummer als String (Format flexibel, z.B. +49...)
    tel = models.CharField(max_length=30, blank=True)

    # Optional: Kurzbeschreibung / Bio
    description = models.TextField(blank=True)

    # Optional: Arbeitszeiten als Text (z.B. "Mo-Fr 9-17")
    working_hours = models.CharField(max_length=50, blank=True)

    # Zeitpunkt der Profilerstellung (wird automatisch gesetzt)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Hilfreich im Django Admin und beim Debugging."""
        return f"{self.user.username} ({self.type})"