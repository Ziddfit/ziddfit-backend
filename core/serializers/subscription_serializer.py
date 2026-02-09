from rest_framework import serializers
from core.models.subscription import GymSubscription

class GymSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = GymSubscription
        fields = '__all__'
        read_only_fields = ['id', 'start_date', 'end_date']