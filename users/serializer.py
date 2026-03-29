from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model  = User
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
            'profile_pic',
            'phone_number',
            'claimed',
        ]
        read_only_fields = [
            'id',
            'email',
            'profile_pic',
            'claimed',
        ]