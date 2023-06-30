from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class ExtendedUserProfile(models.Model):
    """Extend user with additional data."""
    user = models.OneToOneField(User, unique=True, related_name='extended_user_profile', on_delete=models.CASCADE)
    middle_name = models.CharField(max_length=255, blank=True, default='')
