from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


class Offer(models.Model):
    """
    An Offer created by a Business user.

    Contains:
    - Core data (title, description, optional image)
    - Reference to the creator (User)
    - Timestamps used for sorting and filtering

    Note:
    - The three service packages (basic/standard/premium)
      are stored in OfferDetail (related_name='details').
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    image = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)   # creation timestamp
    updated_at = models.DateTimeField(auto_now=True)       # last modification timestamp

    def __str__(self):
        """Improves readability in Django admin and debugging."""
        return f"{self.title} (user={self.user_id})"


class OfferDetail(models.Model):
    """
    Package / pricing details for an Offer.

    In this system, each Offer typically consists of exactly three OfferDetails:
    - basic
    - standard
    - premium

    Intended rules:
    - Each offer_type may exist only once per Offer (enforced via DB constraint).
    - Price and delivery time must be positive values.
    """

    class OfferType(models.TextChoices):
        BASIC = "basic", "Basic"
        STANDARD = "standard", "Standard"
        PREMIUM = "premium", "Premium"

    offer = models.ForeignKey(
        Offer,
        on_delete=models.CASCADE,
        related_name="details"
    )
    title = models.CharField(max_length=255)
    revisions = models.PositiveIntegerField()
    delivery_time_in_days = models.PositiveIntegerField()
    
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    features = models.JSONField(default=list, blank=True)

    offer_type = models.CharField(
        max_length=10,
        choices=OfferType.choices
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["offer", "offer_type"],
                name="unique_offer_type_per_offer",
            )
        ]

    def __str__(self):
        """Improves readability in Django admin and debugging."""
        return f"{self.offer_id}::{self.offer_type} ({self.price}€)"