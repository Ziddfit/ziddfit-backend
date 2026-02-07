from rest_framework import serializers
from core.models.gym_staff import GymStaff

class GymStaffSerializer(erializers.ModelSerializer):
    class Meta:
        model = Gym
        fields = '__all__'