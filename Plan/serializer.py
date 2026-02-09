from rest_framework import serializers
from models import Plan_Subcription, Plan_config
from users.serializer import UserSerializer

class Plan_con_Serializer(serializers.ModelSerializer):
    tier_display = serializers.CharField(source='get_tier_display', read_only=True)

    class Meta:
        model = Plan_config
        fields = [
            'tier', 
            'tier_display', 
            'monthly_price'
        ]

class Plan_sub_Serializer(serializers.ModelSerializer):
    plan = Plan_con_Serializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Plan_Subcription
        fields = [
            'id', 
            'user',
            'plan', 
            'is_active', 
            'expiry_date', 
            'start_date'
        ]