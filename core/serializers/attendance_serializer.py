from rest_framework import serializers
from core.models.attendance import GymAttendance

class GymAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = GymAttendance
        fields = '__all__'
        read_only_fields = ['gym', 'checkin_time', 'date']