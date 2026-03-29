# accounts/views/auth.py
import google.oauth2.id_token
import google.auth.transport.requests

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from django.contrib.auth import get_user_model
from django.conf import settings

from owners.models import Owner
from users.socialauth import SocialAuth
from ..utils import get_tokens_for_user, get_user_role

User = get_user_model()


def set_refresh_cookie(response, refresh_token):
    """Helper — set refresh token as httpOnly cookie"""
    response.set_cookie(
        key='refresh_token',
        value=refresh_token,
        httponly=True,
        secure=not settings.DEBUG,  # False locally, True in production
        samesite='Lax',
        max_age=60 * 60 * 24 * 7,  
    )


class GoogleAuthView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, role='owner'):
        token = request.data.get('id_token')
        if not token:
            return Response(
                {'error': 'id_token is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            google_user = google.oauth2.id_token.verify_oauth2_token(
                token,
                google.auth.transport.requests.Request(),
                settings.GOOGLE_CLIENT_ID
            )
        except ValueError as e:
            return Response(
                {'error': 'Invalid Google token', 'detail': str(e)},
                status=status.HTTP_401_UNAUTHORIZED
            )

        email      = google_user.get('email')
        google_id  = google_user.get('sub')
        first_name = google_user.get('given_name', '')
        last_name  = google_user.get('family_name', '')
        picture    = google_user.get('picture', '')

        if not email:
            return Response(
                {'error': 'Email not provided by Google'},
                status=status.HTTP_400_BAD_REQUEST
            )

        existing_user = User.objects.filter(email=email).first()

        if existing_user:
            if not existing_user.claimed:
                existing_user.claimed = True
                if existing_user.name_set_by_owner:
                    existing_user.first_name = first_name
                    existing_user.last_name  = last_name
                    existing_user.name_set_by_owner = False
                if not existing_user.profile_pic:
                    existing_user.profile_pic = picture
                existing_user.save()

            SocialAuth.objects.get_or_create(
                user=existing_user,
                provider='GOOGLE',
                defaults={'provider_uid': google_id}
            )
            user = existing_user

        else:
            if role != 'owner':
                return Response(
                    {
                        'error': 'No account found.',
                        'detail': 'You must be invited by a gym owner to join.'
                    },
                    status=status.HTTP_403_FORBIDDEN
                )

            user = User.objects.create(
                email=email,
                username=email,
                first_name=first_name,
                last_name=last_name,
                profile_pic=picture,
                claimed=True,
                name_set_by_owner=False,
            )
            user.set_unusable_password()
            user.save()

            SocialAuth.objects.create(
                user=user,
                provider='GOOGLE',
                provider_uid=google_id
            )
            Owner.objects.create(user=user)

        tokens = get_tokens_for_user(user)

        response = Response({
            'access': tokens['access'],
            'user': {
                'id':          str(user.id),
                'email':       user.email,
                'first_name':  user.first_name,
                'last_name':   user.last_name,
                'profile_pic': user.profile_pic,
                'role':        get_user_role(user),
                'claimed':     user.claimed,
            }
        }, status=status.HTTP_200_OK)

        set_refresh_cookie(response, tokens['refresh'])
        return response


class TokenRefreshView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')

        if not refresh_token:
            return Response(
                {'error': 'No refresh token'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        try:
            old_refresh = RefreshToken(refresh_token)

            old_refresh.blacklist()

            user_id = old_refresh['user_id']
            user = User.objects.get(id=user_id)
            tokens = get_tokens_for_user(user)

            response = Response({
                'access': tokens['access']
            })

            set_refresh_cookie(response, tokens['refresh'])
            return response

        except TokenError:
            return Response(
                {'error': 'Invalid or expired token'},
                status=status.HTTP_401_UNAUTHORIZED
            )


class LogoutView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')

        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()       
            except TokenError:
                pass                    

        response = Response({'message': 'Logged out successfully'})
        response.delete_cookie('refresh_token')
        return response
# users/authentication.py
# from rest_framework.authentication import BaseAuthentication
# from django.contrib.auth import get_user_model

# User = get_user_model()

# class JWTAuthentication(BaseAuthentication):
#     def authenticate(self, request):
#         # Return the first user in the database as a dummy user for testing
#         user = User.objects.first()
#         if user:
#             return (user, None)
#         return None