
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Owner
from .serializer import OwnerSerializer


@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def owner_profile(request):
    if request.method == 'POST':
        # Check if user already has an owner profile
        if hasattr(request.user, 'owner_profile') and request.user.owner_profile is not None:
            return Response(
                {'error': 'Owner profile already exists'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = OwnerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    try:
        profile = request.user.owner_profile
    except Owner.DoesNotExist:
        return Response(
            {'error': 'Owner profile not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    if request.method == 'GET':
        serializer = OwnerSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = OwnerSerializer(profile, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PATCH':
        serializer = OwnerSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        profile.delete()
        return Response(
            {'message': 'Owner profile deleted successfully'},
            status=status.HTTP_204_NO_CONTENT
        )