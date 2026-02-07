from django.contrib import admin
from core.models.gym import Gym
from core.models.members import GymMember
from core.models.attendance import GymAttendance

admin.site.register(Gym)
admin.site.register(GymMember)
admin.site.register(GymAttendance)