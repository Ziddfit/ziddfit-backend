from django.db import models
from django.conf import settings
from django.contrib.postgres.indexes import GinIndex
import uuid

class Plan(models.Model):
    PLAN_CHOICES = [
        ('free', 'Free Tier'),
        ('pro', 'Professional'),
        ('enterprise', 'Enterprise'),
    ]
    plan_name = models.CharField(max_length=20, choices=PLAN_CHOICES, default='free')
    is_active = models.BooleanField(default = True)
    start_date = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField(null=True, blank=True)
