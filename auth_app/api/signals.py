from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from auth_app.models import UserProfile

User = get_user_model()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Ensures that each newly created User has a related UserProfile.
    This also covers users created via `createsuperuser`.
    """
    if not created:
        return

    UserProfile.objects.create(
        user=instance,
        email=instance.email or "",
        type=UserProfile.UserType.CUSTOMER,  
    )