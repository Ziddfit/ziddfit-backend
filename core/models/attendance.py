from django.db import models
from django.contrib.postgres.indexes import GinIndex
from core.models.gym import Gym
from core.models.members import GymMember

class GymAttendance(models.Model):
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
    checkin_time = models.DateTimeField(auto_now_add= True)
    entry_source = models.CharField(max_length=50, default='QR_SCAN')
    