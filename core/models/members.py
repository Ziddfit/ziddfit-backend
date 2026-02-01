from django.db import models
from django.conf import settings
#from django.contrib.postgres.indexes import GinIndex
import uuid
from core.models.gym import Gym


class GymMember(models.Model):
    """A gym-specific member record.

    This is a profile-like model that links to the project's user model
    (configured via `AUTH_USER_MODEL`) instead of subclassing
    `AbstractUser`. Only `users.User` should subclass `AbstractUser`.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='gym_profile',
        null=True,
        blank=True,
    )
    gym = models.ForeignKey(
        Gym,
        on_delete=models.CASCADE,
        related_name='members'
    )
    email = models.EmailField(null=True)
    phone = models.CharField(max_length=20)
    membership_start = models.DateField(auto_now_add=True)
    membership_end = models.DateField()

    extra_info = models.JSONField(default=dict, blank=True)

    #class Meta:
    #    indexes = [
    #        GinIndex(fields=['extra_info']),
    #    ]

