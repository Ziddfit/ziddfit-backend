from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
import uuid

class Subscription(models.Model):
    PLAN_CHOICES = [
        ('free', 'Free Tier'),
        ('pro', 'Professional'),
        ('enterprise', 'Enterprise'),
    ]
    plan_name = models.CharField(max_length=20, choices=PLAN_CHOICES, default='free')
    is_active = models.BooleanField(default = False)
    start_date = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField(null=True, blank=True)


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default = uuid.uuid4, editable = False)
    business_name = models.charField(max_length = 255)
    subscription = models.OneToOneField(
        Subscription, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='owner'
    )
    business_name = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    email_id = models.EmailField(max_length=254)


class Gym(models.Model):
    id = models.UUIDField(primary_key=True, default = uuid.uuid4, editable= False)
    owner = models.ForeignKey(User, 
        on_delete= models.CASCADE,
        related_name= 'gyms'
    )
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add= True)
