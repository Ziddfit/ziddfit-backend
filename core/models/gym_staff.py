import uuid
from django.db import models
from django.conf import settings
from ..models.gym import Gym 

class GymStaff(models.Model):
    ROLE_CHOICES = [
        ('MANAGER', 'Manager'),
        ('TRAINER', 'Trainer'),
        ('RECEPTIONIST', 'Receptionist'),
        ('CLEANER', 'Cleaner'),
        ('SECURITY', 'Security'),
        ('OTHER', 'Other'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='staff_profile',
        null=True,
        blank=True
    )

    gym = models.ForeignKey(
        Gym,
        on_delete=models.CASCADE,
        related_name='staff'
    )

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
        # Since 'user' handles the unique identity now, 
        # we index gym and role for fast searching.
        indexes = [
            models.Index(fields=['gym', 'role']),
        ]

    def __str__(self):
        return f"{self.user.email if self.user else 'Unlinked Staff'} - {self.role}"