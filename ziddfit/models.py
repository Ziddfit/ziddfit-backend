from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
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


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default = uuid.uuid4, editable = False)
    business_name = models.charField(max_length = 255)
    subscription = models.OneToOneField(
        Plan, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='owner'
    )
    phone_number = models.CharField(max_length=15, blank=True)
    email_id = models.EmailField(max_length=254)


class Gym(models.Model):
    id = models.UUIDField(primary_key=True, default = uuid.uuid4, editable= False)
    owner = models.ForeignKey(
        User, 
        on_delete= models.CASCADE,
        related_name= 'gyms'
    )
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add= True)


class GymMember(AbstractUser):
    id = models.UUIDField(primary_key= True, default = uuid.uuid4, editable= False)
    gym = models.ForeignKey(
        Gym, 
        on_delete=models.CASCADE, 
        related_name='members'
    )
    first_name = models.CharField(max_length= 100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField( null= True)
    phone = models.CharField(max_length=20)
    membership_start = models.DateField(auto_now_add=True)
    membership_end = models.DateField()


    extra_info = models.JSONField(default=dict, blank=True)
    class Meta:
        indexes = [
            GinIndex(fields=['extra_info']),
        ]


class GymAttendence(models.Model):
    gym = models.ForeignKey(
        Gym, 
        on_delete= models.CASCADE,
        related_name = 'gymattends'
    )
    user = models.ForeignKey(
        GymMember,
        on_delete = models.CASCADE,
        related_name= 'memattends'
    )
    checkin_Time = models.DateTimeField(auto_now_add= True)
    entry_source = models.CharField(max_length=50, default='QR_SCAN')


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
