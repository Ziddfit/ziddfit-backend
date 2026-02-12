import uuid
from django.db import models
from django.conf import settings
from ..models.gym import Gym

class GymMember(models.Model):
    """
    A gym-specific member profile. 
    Links a Global User to a specific Gym and handles subscription/tracking.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='gym_profile',
        help_text="The global identity associated with this gym membership."
    )

    gym = models.ForeignKey(
        Gym,
        on_delete=models.CASCADE,
        related_name='members'
    )

    membership_start = models.DateField(auto_now_add=True)
    membership_end = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    extra_info = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"{self.user.email} - {self.gym.name}"

    class Meta:
        indexes = [
            models.Index(fields=['membership_end']),
        ]