from rest_framework import serializers
from .models import Owner
from users.serializer import UserSerializer

class OwnerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Owner
        fields = [
            'user',
            'business_name',
            'tax_id'
        ]

