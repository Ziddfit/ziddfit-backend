from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from serializer import UserSerializer
from rest_framework import status 


@api_view(['GET'])
def user_Profile(request):
    user = request.user
    serializer = UserSerializer(user)

    return Response(serializer.data, status = status.HTTP_200_OK)
