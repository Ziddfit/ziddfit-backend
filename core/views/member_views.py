from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from core.models.gym import Gym
from core.models.members import GymMember
from core.serializers.member_serializer import GymMemberSerializer
import datetime
from django.utils import timezone


#this is the gym member CREATE and READ function
@api_view(['GET', 'POST'])
def member_list(request):
    if request.method == 'GET':
        gym_id = request.query_params.get('gym_id')
        active = request.query_params.get('active')

        try:
            
            members = GymMember.objects.filter(gym__owner=request.user)
            if gym_id:
                members = members.filter(gym__id =gym_id)
            if active == 'true':
                members = members.filter(membership_end__gte= timezone.now())

            serializer = GymMemberSerializer(members, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": "Retrieval failed", "details": str(e)},
                status = status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    elif request.method == 'POST':
        try:
            serializer = GymMemberSerializer(data=request.data)
            if serializer.is_valid():
                gym = serializer.validated_data.get('gym')
                if gym.owner != request.user:
                    return Response(
                        {"error": "You do not have permission to add members to this gym."},
                        status=status.HTTP_403_FORBIDDEN
                    )
                serializer.save()
                return Response(
                    serializer.data,
                    status = status.HTTP_201_CREATED
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response(
                {"error": "Creation failed", "details": str(e)},
                status = status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        

@api_view(['GET', 'PATCH'])
def member_profile(request, memberid):
    member = get_object_or_404(GymMember, id = memberid, gym__owner = request.user)

    if request.method == 'GET':
        try:
            serializer = GymMemberSerializer(member)

            return Response(serializer.data, status = status.HTTP_200_OK)
        except Exception as e:
            return Response({ 'error' : 'retrieval failed', 'details' : str(e)}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    elif request.method == 'PATCH':
        try:
            serializer = GymMemberSerializer(member, request.data, partial = True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status = status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({ 'error' : 'update failed', 'details' : str(e)}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)
            
