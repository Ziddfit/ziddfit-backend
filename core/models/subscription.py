from django.db import models
from django.conf import settings
from django.contrib.postgres.indexes import GinIndex
import uuid
from core.models.gym import Gym
from core.models.members import GymMember

class GymSubscription(models.Model):
    PLAN_TYPE = [
        ('MONTHLY', 'Monthly'),
        ('QUARTERLY', 'Quarterly'),
        ('HALFYEARLY', 'Half-Yearly'),
        ('YEARLY', 'Yearly'),
        ('CUSTOM', 'Custom'),
    ]
    id = models.UUIDField(primary_key= True, default = uuid.uuid4, editable= False)
    time_period = models.PositiveIntegerField(help_text="Duration of the plan in days")
    description = models.CharField(max_length = 250)
    member = models.OneToOneField(
        GymMember,
        on_delete=models.SET_NULL,
        null=True, 
        blank=True,
        related_name='subscription'
    )
    plan_type = models.CharField(
        max_length=20,
        choices=PLAN_TYPE,
        default='MONTHLY'
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.PositiveIntegerField(help_text = "current available discount")
    is_active = models.BooleanField(default = True)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(null=True, blank=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['member', 'plan_type']),
        ]
