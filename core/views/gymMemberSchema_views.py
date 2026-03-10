from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from core.models.members import GymMemberFieldSchema
from core.serializers.member_serializer import MemberFieldSerializer

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def member_schema_list(request, gymid):
    if request.method == 'GET':
        try:
            Fields = GymMemberFieldSchema.objects.filter(gym = gymid)
            serializer = MemberFieldSerializer(Fields, many = True)
            return Response( serializer.data, status = status.HTTP_200_OK)
        
        except Exception as e:
            return Response({ 'error' : 'retrieval failed', 'details' : str(e)}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    
    elif request.method == 'POST':
        try:
            serializer = MemberFieldSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save(gym = gymid)
                return Response( serializer.data, status = status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({
                'error' : 'creation of field failed',
                'details' : str(e)
            },
            status = status.HTTP_500_INTERNAL_SERVER_ERROR)
