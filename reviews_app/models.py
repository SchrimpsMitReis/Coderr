from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Review(models.Model):
    """
    Review model for Business users.

    Relationships:
    - business_user: The provider being reviewed
    - reviewer: The user (typically a Customer) who submits the review

    Rules:
    - A reviewer may review a specific Business user only once
      (enforced via a UniqueConstraint in Meta)    """

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

    rating = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ]
    )

    description = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["reviewer", "business_user"],
                name="unique_review_per_reviewer_business",
            )
        ]

    def __str__(self):
        return f"Review {self.id}: {self.reviewer_id} -> {self.business_user_id} ({self.rating})"