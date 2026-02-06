from django.db import models
from django.conf import settings
import uuid
from core.models.gym import Gym

class GymStaff(models.Model):
    ROLE_CHOICES = [
        ('OWNER', 'Owner'),
        ('MANAGER', 'Manager'),
        ('TRAINER', 'Trainer'),
        ('RECEPTIONIST', 'Receptionist'),
        ('CLEANER', 'Cleaner'),
        ('SECURITY', 'Security'),
        ('OTHER', 'Other'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    gym = models.ForeignKey(
        Gym,
        on_delete=models.CASCADE,
        related_name='staff'
    )

    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField(null=True, blank=True)

    role = models.CharField(
        max_length=30,
        choices=ROLE_CHOICES
    )
    
    salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    shift_start = models.TimeField(null=True, blank=True)
    shift_end = models.TimeField(null=True, blank=True)

    is_active = models.BooleanField(default=True)
    
    extra_info = models.JSONField(default=dict, blank=True)

    class Meta:
        unique_together = ('gym', 'phone')
        indexes = [
            models.Index(fields=['gym', 'role']),
        ]
