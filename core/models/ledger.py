import uuid
from django.db import models
from django.conf import settings
from ..models.gym import Gym

class LedgerEntry(models.Model):
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

    CATEGORIES = []
    category = models.CharField(max_length=20, choices=CATEGORIES)

