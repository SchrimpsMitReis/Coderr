from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


class Offer(models.Model):
    """
    Ein Offer (Angebot) eines Business-Users.

    Enthält:
    - Stammdaten (Titel, Beschreibung, optionales Bild)
    - Verknüpfung zum Ersteller (User)
    - Zeitstempel für Sortierung/Filter

    Hinweis:
    - Die drei Pakete (basic/standard/premium) liegen in OfferDetail (related_name='details').
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)

    # Optionales Bild (URL oder Dateiname).
    # Empfehlung: entweder blank=True und default="" ODER null=True vermeiden -> konsistent halten.
    image = models.CharField(max_length=255, blank=True, null=True)

    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)   # Erstellung
    updated_at = models.DateTimeField(auto_now=True)       # letzte Änderung

    def __str__(self):
        """Hilfreich im Admin & Debugging."""
        return f"{self.title} (user={self.user_id})"


class OfferDetail(models.Model):
    """
    Detail-/Paket-Informationen zu einem Offer.

    Ein Offer besteht in deinem System typischerweise aus exakt drei OfferDetails:
    - basic
    - standard
    - premium

    Regeln (Soll-Zustand):
    - Pro Offer darf jeder offer_type nur einmal existieren (DB-Constraint empfohlen).
    - Preis und Lieferzeit sind positive Werte.
    """

    class OfferType(models.TextChoices):
        BASIC = "basic", "Basic"
        STANDARD = "standard", "Standard"
        PREMIUM = "premium", "Premium"

    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name="details")

    title = models.CharField(max_length=255)
    revisions = models.PositiveIntegerField()
    delivery_time_in_days = models.PositiveIntegerField()

    # Preis: DecimalField ist korrekt.
    # Optional: MinValueValidator(0) oder >0 erzwingen.
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )

    # Features: Liste von Strings (z.B. ["Logo Design", "Flyer"])
    # JSONField ist OK fürs Lernprojekt.
    features = models.JSONField(default=list, blank=True)

    offer_type = models.CharField(max_length=10, choices=OfferType.choices)

    class Meta:
        # Stellt sicher: pro Offer existiert jedes Paket (basic/standard/premium) max. 1x
        constraints = [
            models.UniqueConstraint(
                fields=["offer", "offer_type"],
                name="unique_offer_type_per_offer",
            )
        ]

    def __str__(self):
        """Hilfreich im Admin & Debugging."""
        return f"{self.offer_id}::{self.offer_type} ({self.price}€)"

