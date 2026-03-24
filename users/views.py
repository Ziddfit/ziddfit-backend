from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .serializer import UserSerializer


@api_view(['GET', 'PATCH'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    user = request.user

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'PATCH':
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_profile_pic(request):
    file = request.FILES.get('profile_pic')

    if not file:
        return Response(
            {'error': 'profile_pic file is required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # TODO: upload to S3 / Cloudinary and get back a URL
    # url = upload_to_s3(file)
    # request.user.profile_pic = url
    # request.user.save()
    # return Response({'profile_pic': url})

    return Response(
        {'message': 'Upload logic not yet implemented'},
        status=status.HTTP_501_NOT_IMPLEMENTED
    )
