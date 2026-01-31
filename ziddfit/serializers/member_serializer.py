from rest_framework import serializers
from ..models import GymMember

class GymMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = GymMember
        fields = '__all__'