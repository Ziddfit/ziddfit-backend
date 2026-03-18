import uuid
from django.db import models
from django.conf import settings
from ..models.gym import Gym
from ..models.members import GymMember
from ..models.gym_staff import GymStaff

class Transaction(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length= 255)
    gym = models.ForeignKey(
        Gym,
        on_delete=models.CASCADE,
        related_name='ledgers'
    )
    TRANSACTION_TYPE = [
        ("credit", "Credit"),
        ("debit",  "Debit"),
    ]
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE)
    amount = models.PositiveIntegerField()   
    CATEGORIES = []
    category = models.CharField(max_length=20, choices=CATEGORIES)
    PARTY_TYPE = ['gymmember', 'staff', 'vendor', 'other']
    party_name = models.CharField(max_length=255)       
    party_type = models.CharField(max_length=20, choices= PARTY_TYPE)         
    member = models.ForeignKey(GymMember, null=True, blank=True, on_delete=models.SET_NULL)
    staff  = models.ForeignKey(GymStaff, null=True, blank=True, on_delete=models.SET_NULL)
    is_reversal = models.BooleanField(default = False)
    reversal_of = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    created_at = models.DateTimeField(auto_now_add= True)
    metadata = models.JSONField( default = dict, blank = True)