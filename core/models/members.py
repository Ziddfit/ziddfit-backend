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
        unique_together = [['user', 'gym']]




class gymMemberFieldSchema(models.Model):
    FIELD_TYPES = [
        ("text",        "Text"),
        ("number",      "Number"),
        ("date",        "Date (YYYY-MM-DD)"),
        ("boolean",     "Boolean (Yes / No)"),
        ("select",      "Single Select"),
        ("multiselect", "Multi Select"),
        ("file",        "File Upload URL"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    gym = models.ForeignKey(
        Gym,
        on_delete=models.CASCADE,
        related_name="member_field_schema"
    )

    field_label   = models.CharField(max_length=255)          
    field_type    = models.CharField(max_length=20, choices=FIELD_TYPES, default="text")
    is_required   = models.BooleanField(default=False)
    is_active     = models.BooleanField(default=True)         # soft-delete


    # Only for "select" / "multiselect" types
    # e.g. ["White", "Blue", "Purple", "Brown", "Black"]
    options = models.JSONField(default=list, blank=True)

    validation_rules = models.JSONField(default= dict, blank= True)

    display_order = models.PositiveSmallIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [["gym", "field_key"]]
        ordering = ["display_order", "created_at"]

    def __str__(self):
        return f"{self.gym.name} | {self.field_label} ({self.field_type})"