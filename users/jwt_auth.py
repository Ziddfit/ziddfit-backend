from rest_framework import exceptions
from rest_framework_simplejwt.authentication import JWTAuthentication as SimpleJWTAuthentication
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError

from django.contrib.auth import get_user_model

User = get_user_model()


def verify_access_token(token):
    """Verify raw access token and return user instance."""
    if not token:
        raise exceptions.AuthenticationFailed('No access token provided')

    try:
        access = AccessToken(token)
    except TokenError as e:
        raise exceptions.AuthenticationFailed(f'Invalid token: {str(e)}')

    user_id = access.get('user_id')
    if not user_id:
        raise exceptions.AuthenticationFailed('Token missing user information')

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise exceptions.AuthenticationFailed('User not found for token')

    if not user.is_active:
        raise exceptions.AuthenticationFailed('User is inactive')

    return user


class JWTAuthentication(SimpleJWTAuthentication):
    """Custom JWT authentication for DRF request.user population."""

    def authenticate(self, request):
        header = self.get_header(request)
        if header is None:
            access_token = request.COOKIES.get('access_token')
            if access_token:
                user = verify_access_token(access_token)
                return (user, None)
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)
        user = self.get_user(validated_token)

        if user is None or not user.is_active:
            raise exceptions.AuthenticationFailed('User inactive or deleted')

        return (user, validated_token)
