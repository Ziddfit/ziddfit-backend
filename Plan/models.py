from django.db import models
from django.conf import settings

class Plan_config(models.Model):
    tier = models.CharField(max_length=20,unique=True)
    monthly_price = models.DecimalField(max_digits=10,decimal_places=2)

class Plan_Subcription(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='plan_subcription'
    )
    plan = models.ForeignKey(Plan_config,on_delete=models.PROTECT)
    is_active = models.BooleanField(default=True)
    
