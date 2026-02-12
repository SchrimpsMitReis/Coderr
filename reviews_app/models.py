from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.


class Review(models.Model):
    """
    Bewertungsmodell für Business-User.

    Beziehungen:
    - business_user: Der Anbieter, der bewertet wird
    - reviewer: Der User (i.d.R. Customer), der die Bewertung abgibt

    Regeln:
    - Ein Reviewer darf ein Business nur einmal bewerten
      (UniqueConstraint in Meta)
    """

    business_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="received_reviews",
    )

    reviewer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="written_reviews",
    )

    # Bewertung (z.B. 1–5 Sterne)
    rating = models.IntegerField(
        # Optional, aber sinnvoll:
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ]
    )

    description = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """
        Stellt sicher:
        - Ein Reviewer kann ein Business nur einmal bewerten.
        """
        constraints = [
            models.UniqueConstraint(
                fields=["reviewer", "business_user"],
                name="unique_review_per_reviewer_business",
            )
        ]

    def __str__(self):
        """
        Lesbare Darstellung für Admin und Debugging.
        """
        return f"Review {self.id}: {self.reviewer_id} -> {self.business_user_id} ({self.rating})"