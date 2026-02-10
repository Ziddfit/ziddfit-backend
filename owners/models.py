from django.db import models
from users.models import User

class Owner(User):

    business_name = models.CharField(max_length= 255)
    tax_id = models.CharField(max_length=50, unique=True, null=True)

    class Meta:
        verbose_name = "Gym Owner"
        db_table = "owners_owner"