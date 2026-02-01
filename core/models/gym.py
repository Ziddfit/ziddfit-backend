from django.db import models
from django.conf import settings
from django.contrib.postgres.indexes import GinIndex
import uuid
from users.models import User

class Gym(models.Model):
    id = models.UUIDField(primary_key=True, default = uuid.uuid4, editable= False)
    owner = models.ForeignKey(
        User, 
        on_delete= models.CASCADE,
        related_name= 'gyms'
    )
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add= True)

