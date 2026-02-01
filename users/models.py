from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.indexes import GinIndex
import uuid


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default = uuid.uuid4, editable = False)
    business_name = models.CharField(max_length = 255)
    subscription = models.OneToOneField(
        'Plan.Plan', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='owner'
    )
    phone_number = models.CharField(max_length=15, blank=True)
    email_id = models.EmailField(max_length=254)
