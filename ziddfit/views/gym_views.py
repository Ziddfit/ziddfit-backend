from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from ..models import GymMember, Gym
from ..serializers.gym_serializer import GymSerializer


@api_view(['GET', 'POST'])
def gym_list(request):
    if request.method == 'GET':
        try:
            gyms = Gym.objects.filter(owner = request.user)
            serializer = GymSerializer(gyms, many=True)

            return Response( serializer.data, status = status.HTTP_200_OK)
        except Exception as e:
            return Response({ 'error' : 'retrieval failed', 'details' : str(e)}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    elif request.method == 'POST':
        try:
            serializer = GymSerializer(data = request.data)
            if serializer.is_valid:
                serializer.save(owner=request.user)
                return Response( serializer.data, status = status.HTTP_201_CREATED)
                
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(
                {"error": "Creation failed", "details": str(e)},
                status = status.HTTP_500_INTERNAL_SERVER_ERROR
            )