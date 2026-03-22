from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from core.models.gym import Gym
from django.db.models import Q
from core.models.members import GymMember, GymMemberFieldSchema
from core.serializers.member_serializer import GymMemberSerializer, CreateMemberSerializer
from django.utils import timezone
from utils.pagination import StandardResultsPagination
from users.models import User
import uuid


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def member_list(request, gym_id):
    gym = get_object_or_404(Gym, id=gym_id, owner=request.user.owner_profile)

    if request.method == 'GET':
        try:
            active = request.query_params.get('active')
            search = request.query_params.get('search')

            members = GymMember.objects.filter(gym=gym)

            if active:
                if active.lower() == 'true':
                    members = members.filter(membership_end__gte=timezone.now().date())
                elif active.lower() == 'false':
                    members = members.filter(membership_end__lte=timezone.now().date())

            if search:
                members = members.filter(
                    Q(user__first_name__icontains=search) |
                    Q(user__last_name__icontains=search) |
                    Q(user__phone_number__icontains=search)
                )

            schema_keys = GymMemberFieldSchema.objects.filter(
                gym=gym, is_active=True
            ).values_list('field_key', flat=True)

            for key in schema_keys:
                value = request.query_params.get(key)
                if value:
                    members = members.filter(extra_info__contains={key: value})

            paginator = StandardResultsPagination()
            paginated_qs = paginator.paginate_queryset(members, request)
            serializer = GymMemberSerializer(paginated_qs, many=True)
            return paginator.get_paginated_response(serializer.data)

        except Exception as e:
            return Response(
                {"error": "Retrieval failed", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    elif request.method == 'POST':
        try:
            serializer = CreateMemberSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            data = serializer.validated_data
            email = data.get('email')

            if email:
                user = User.objects.filter(email=email).first()
                if user:
                    if GymMember.objects.filter(user=user, gym=gym).exists():
                        return Response(
                            {"error": "This user is already a member of this gym."},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                else:
                    user = User.objects.create(
                        email=email,
                        username=email,
                        first_name=data.get('first_name', ''),
                        last_name=data.get('last_name', ''),
                        phone_number=data.get('phone_number'),
                        claimed=False,
                    )
                    user.set_unusable_password()
                    user.save()
            else:
                placeholder_email = f"member_{uuid.uuid4().hex[:8]}@placeholder.local"
                user = User.objects.create(
                    email=placeholder_email,
                    username=placeholder_email,
                    first_name=data.get('first_name', ''),
                    last_name=data.get('last_name', ''),
                    phone_number=data.get('phone_number'),
                    claimed=False,
                )
                user.set_unusable_password()
                user.save()

            member = GymMember.objects.create(
                user=user,
                gym=gym,
                membership_end=data.get('membership_end'),
                extra_info=data.get('extra_info', {}),
            )

            response_serializer = GymMemberSerializer(member)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {"error": "Creation failed", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@api_view(['GET', 'PATCH'])
@permission_classes([IsAuthenticated])
def member_profile(request, gym_id, member_id):
    gym = get_object_or_404(Gym, id=gym_id, owner=request.user.owner_profile)
    member = get_object_or_404(GymMember, id=member_id, gym=gym)

    if request.method == 'GET':
        try:
            serializer = GymMemberSerializer(member)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": "Retrieval failed", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    elif request.method == 'PATCH':
        try:
            serializer = GymMemberSerializer(member, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": "Update failed", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )