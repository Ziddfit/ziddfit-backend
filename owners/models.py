from django.db import models
from django.conf import settings
from users.models import User

class Owner(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='owner_profile'
    )
    business_name = models.CharField(max_length= 255)
    tax_id = models.CharField(max_length=50, unique=True, null=True)

    class Meta:
        verbose_name = "Gym Owner"
        db_table = "owners_owner"
    def __str__(self):
        return self.user.email    