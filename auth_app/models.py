from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """
    Extension profile for the Django `User` model.

    Purpose:
    - Separates authentication data (User: username/password)
      from profile-specific data.
    - Stores the profile type (Customer/Business) used for
      permissions and business logic.
    - Contains optional profile information
      (name, phone, location, description, working hours).

    Notes:
    - `user` is a OneToOne relationship → exactly one profile per User.
    - `type` is typically set during registration and later used
    for authorization and business rules.    """

    class UserType(models.TextChoices):
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
        return f"{self.user.username} ({self.type})"