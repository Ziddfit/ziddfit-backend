from django.db import models
from django.conf import settings
import uuid

class Plan_config(models.Model):
    PLAN_CHOICES = [
        ('starter', 'Starter'),
        ('pro', 'Professional'),
        ('enterprise', 'Enterprise'),
    ]
    tier = models.CharField(max_length=20, choices=PLAN_CHOICES, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.PositiveIntegerField()
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.tier

class Plan_Subcription(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='plan_subcription'
    )
    plan = models.ForeignKey(Plan_config,on_delete=models.PROTECT)
    is_active = models.BooleanField(default=True)
    start_date = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField(null=True, blank=True)
    class Meta:
        indexes = [
            models.Index(fields=['is_active']),
            models.Index(fields=['expiry_date']),
        ]
    def __str__(self):
        return f"{self.user.email} - {self.plan.tier}"
