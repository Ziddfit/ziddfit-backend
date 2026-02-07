from rest_framework import serializers
from models import Plan_Subcription, Plan_config

class Plan_sub_Serializer(serializers.ModelSerializer):
    
    class Meta:
        model = Plan_Subcription
        fields = '__all__'

class Plan_con_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Plan_config
        fields = '__all__'