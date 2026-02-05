from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.indexes import GinIndex
import uuid

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True) 
    
    first_name = models.charField(max_length = 255, blank = True)
    last_name = models.charField(max_length = 255, blank = True)

    business_name = models.CharField(max_length=255, blank=True)

    profile_pic = models.charField(max_length = 1000, blank = True)
    
    subscription = models.ForeignKey(
        'Plan.Plan', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='users'
    )
    
    phone_number = models.CharField(
        max_length=15,
        unique=True,
        null=True,
        blank=True,
        default=None 
    )
    
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email