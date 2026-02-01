from rest_framework import serializers
from core.models.gym import Gym

class GymSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gym
        fields = '__all__'