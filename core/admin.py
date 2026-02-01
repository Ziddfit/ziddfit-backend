from django.contrib import admin
from core.models.gym import Gym
from core.models.members import GymMember
from core.models.attendence import GymAttendence

admin.site.register(Gym)
admin.site.register(GymMember)
admin.site.register(GymAttendence)