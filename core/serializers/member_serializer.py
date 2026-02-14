from rest_framework import serializers
from core.models.members import GymMember

class GymMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = GymMember
        fields = '__all__'
        read_only_fields = ['id', 'gym', 'membership_start']
