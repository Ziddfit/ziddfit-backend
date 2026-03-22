from django.contrib import admin
from core.models.gym import Gym
from core.models.members import GymMember, GymMemberFieldSchema
from core.models.attendance import GymAttendance
from core.models.subscription import GymSubscription


admin.site.register(Gym)
admin.site.register(GymMember)
admin.site.register(GymAttendance)
admin.site.register(GymMemberFieldSchema)
admin.site.register(GymSubscription)