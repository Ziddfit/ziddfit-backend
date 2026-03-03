from rest_framework import serializers
from core.models.gym_staff import GymStaff

class GymStaffSerializer(erializers.ModelSerializer):
    class Meta:
        model = GymStaff 
        fields = '__all__'
        read_only_fields = ['id', 'gym']