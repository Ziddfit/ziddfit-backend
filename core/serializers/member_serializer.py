from rest_framework import serializers
from core.models.members import GymMember, GymMemberFieldSchema


class CreateMemberSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255, required=False, default='')
    email = serializers.EmailField(required=False, allow_null=True)
    phone_number = serializers.CharField(max_length=15, required=False, allow_null=True)
    membership_end = serializers.DateField(required=False, allow_null=True)
    extra_info = serializers.DictField(required=False, default=dict)


class GymMemberSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    phone_number = serializers.CharField(source='user.phone_number', read_only=True)

    class Meta:
        model = GymMember
        fields = [
            'id', 'gym', 'user',
            'first_name', 'last_name', 'email', 'phone_number',
            'membership_start', 'membership_end',
            'is_active', 'extra_info'
        ]
        read_only_fields = ['id', 'gym', 'user', 'membership_start', 'is_active',
                            'first_name', 'last_name', 'email', 'phone_number']


class MemberFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = GymMemberFieldSchema
        fields = '__all__'
        read_only_fields = ['id', 'gym', 'created_at']