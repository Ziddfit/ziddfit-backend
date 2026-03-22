# core/models/subscription.py
from django.db import models
import uuid
from core.models.gym import Gym

class GymSubscription(models.Model):
    PLAN_TYPE = [
        ('MONTHLY', 'Monthly'),
        ('QUARTERLY', 'Quarterly'),
        ('HALFYEARLY', 'Half-Yearly'),
        ('YEARLY', 'Yearly'),
        ('CUSTOM', 'Custom'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE, related_name='subscription_plans')
    time_period = models.PositiveIntegerField(help_text="Duration of the plan in days")
    description = models.CharField(max_length=250)
    plan_type = models.CharField(max_length=20, choices=PLAN_TYPE, default='MONTHLY')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percent = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_default = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['gym', 'plan_type']),
        ]

    def __str__(self):
        return f"{self.gym.name} - {self.plan_type}"