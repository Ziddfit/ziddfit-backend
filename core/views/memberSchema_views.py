from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from core.models.members import GymMemberFieldSchema
from core.models.gym import Gym
from core.serializers.member_serializer import MemberFieldSerializer

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def member_schema_list(request, gym_id):
    gym = get_object_or_404(Gym, pk=gym_id)
    if request.method == 'GET':
        try:
            Fields = GymMemberFieldSchema.objects.filter(gym = gym_id)
            serializer = MemberFieldSerializer(Fields, many = True)
            return Response( serializer.data, status = status.HTTP_200_OK)
        
        except Exception as e:
            return Response({ 'error' : 'retrieval failed', 'details' : str(e)}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    
    elif request.method == 'POST':
        try:
            serializer = MemberFieldSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save(gym = gym)
                return Response( serializer.data, status = status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({
                'error' : 'creation of field failed',
                'details' : str(e)
            },
            status = status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['PUT','PATCH','DELETE'])
@permission_classes([IsAuthenticated])
def member_schema_detail(request, gym_id, field_id):
    schema_field = get_object_or_404(GymMemberFieldSchema, gym = gym_id, id = field_id)
    try:

        if request.method == 'PATCH':
            serializer = MemberFieldSerializer(schema_field, data = request.data, partial = True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status = status.HTTP_200_OK)     
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)                

        if request.method == 'PUT':
            serializer = MemberFieldSerializer(schema_field, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        if request.method == 'DELETE':
            schema_field.delete()
            return Response({"message : The metadata field has been successfully deleted"}, status = status.HTTP_204_NO_CONTENT)
        
        
    except Exception as e:
        return Response({
                'error' : 'creation of field failed',
                'details' : str(e)
            },
            status = status.HTTP_500_INTERNAL_SERVER_ERROR
        )


