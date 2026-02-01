from django.db import models
from django.conf import settings
from django.contrib.postgres.indexes import GinIndex
import uuid
from core.models.gym import Gym
from core.models.members import GymMember

class GymSubscription(models.Model):
    id = models.UUIDField(primary_key= True, default = uuid.uuid4, editable= False)
    Time_period = models.PositiveIntegerField(help_text="Duration of the plan in days")
    Description = models.CharField(max_length = 250)
    member = models.OneToOneField(
        GymMember,
        on_delete=models.SET_NULL,
        null=True, 
        blank=True,
        related_name='subscription'
    )
    discount = models.PositiveIntegerField(help_text = "current available discount")
    is_Active = models.BooleanField(default = True)
