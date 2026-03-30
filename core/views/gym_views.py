from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from core.models.gym  import Gym
from core.serializers.gym_serializer import GymSerializer

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def gym_list(request):
    if request.method == 'GET':
        try:
            # Check if user has owner profile
            if not hasattr(request.user, 'owner_profile') or request.user.owner_profile is None:
                return Response(
                    {'error': 'Owner profile required to view gyms. Create one at POST /api/owners/owner/'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            gyms = Gym.objects.filter(owner = request.user.owner_profile)
            serializer = GymSerializer(gyms, many=True)
            return Response( serializer.data, status = status.HTTP_200_OK)
        except Exception as e:
            return Response({ 'error' : 'retrieval failed', 'details' : str(e)}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    elif request.method == 'POST':
        try:
            # Check if user has owner profile
            if not hasattr(request.user, 'owner_profile') or request.user.owner_profile is None:
                return Response(
                    {'error': 'Owner profile required to create gyms. Create one at POST /api/owners/owner/'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            serializer = GymSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save(owner=request.user.owner_profile)
                return Response( serializer.data, status = status.HTTP_201_CREATED)
                
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(
                {"error": "Creation failed", "details": str(e)},
                status = status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@api_view(['PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def gym_detail(request, gym_id):
    # Check if user has owner profile
    if not hasattr(request.user, 'owner_profile') or request.user.owner_profile is None:
        return Response(
            {'error': 'Owner profile required to manage gyms. Create one at POST /api/owners/owner/'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    gym = get_object_or_404(Gym, pk=gym_id, owner=request.user.owner_profile)
    if request.method == 'GET':
        serializer = GymSerializer(gym)
        return Response(serializer.data)
    
    if request.method == 'PATCH':
        serializer = GymSerializer(gym, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'PUT':
        serializer = GymSerializer(gym, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'DELETE':
        gym.delete()
        return Response({"message": "Gym deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    

