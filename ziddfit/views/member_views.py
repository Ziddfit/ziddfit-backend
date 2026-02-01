from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from ..models import GymMember, Gym
from ..serializers.member_serializer import GymMemberSerializer


#this is the gym member CREATE and READ function
@api_view(['GET', 'POST'])
def member_list(request):
    if request.method == 'GET':
        try:
            members = GymMember.objects.filter( Gym__owner = request.user)
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
            if serializer.is_valid:
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
        

@api_view(['PATCH', 'UPDATE', 'DELETE'])
def gym_detail(request, pk):
    pass