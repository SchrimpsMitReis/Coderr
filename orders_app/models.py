from django.db import models
from django.contrib.auth.models import User

class Orders(models.Model):

    class OfferType(models.TextChoices):
        BASIC = "basic", "Basic"
        STANDARD = "standard", "Standard"
        PREMIUM = "premium", "Premium"

    class StatusType(models.TextChoices):
        IN_PROGRESS = "in_progress"
        COMPLETED = "completed"
        CANCELLED = "cancelled"

    customer_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order_orderer')
    business_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='offer_owner')
    title = models.CharField(max_length=255)
    revisions = models.IntegerField()
    delivery_time_in_days = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.JSONField(default=list, blank=True)
    offer_type = models.CharField(max_length=10, choices=OfferType)
    status = models.CharField(max_length=15, choices=StatusType)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
