from django.shortcuts import render
from rest_frameworks.permissions import IsAuthenticated
from rest_framework.decorators import api_view,permission_classes
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_frameworks.response import Response
from models import Owner
from serializer import OwnerSerializer

@api_view(['GET','POST','PUT'])
@permission_classes([IsAuthenticated])
def owner_profile(request):


    if request.method == 'GET':
        try:
            serializer = OwnerSerializer(request.user.owner_profile)
            return Response(serializer.data, status = status.HTTPS_200_OK)
        except Owner.DoesNotExist:
            return Response(
                {"error": "Owner profile does not exist for this user."}, 
                status=status.HTTP_404_NOT_FOUND
            )
        

    elif request.method == 'POST':
        serializer = OwnerSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save(user = request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    elif request.method == 'PUT':
        try:
            profile = request.user.owner_profile
        except Owner.DoesNotExist:
            return Response({"error": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = OwnerSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH','DELETE']) 
@permission_classes([IsAuthenticated])
def update_owner_profile(request):
    if request.method == 'PATCH':
        try:
            profile = request.user.owner_profile 
        except Owner.DoesNotExist:
            return Response({"error": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = OwnerSerializer(profile, data=request.data, partial=True)
    
        if serializer.is_valid():
            serializer.save() 
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        try:
            profile = request.user.owner_profile
            profile.delete()
            return Response(
                {"message": "Owner profile deleted successfully."}, 
                status=status.HTTP_204_NO_CONTENT
            )
            
        except Owner.DoesNotExist:
            return Response(
                {"error": "Profile not found or already deleted."}, 
                status=status.HTTP_404_NOT_FOUND
            )