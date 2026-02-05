# authentication.py

import jwt
from jwt import PyJWKClient
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

class SupabaseAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None

        try:
            prefix, token = auth_header.split()
            if prefix.lower() != 'bearer':
                raise AuthenticationFailed('Authorization header must start with Bearer')
        except ValueError:
            raise AuthenticationFailed('Invalid Authorization header format')

        try:
            payload = self.verify_token(token)
        except Exception as e:
            raise AuthenticationFailed(f"Invalid token: {str(e)}")

        return self.get_or_create_user(payload)

    def verify_token(self, token):
        jwks_url = f"{settings.SUPABASE_URL}/auth/v1/keys"
        jwks_client = PyJWKClient(jwks_url)
        signing_key = jwks_client.get_signing_key_from_jwt(token)

        return jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            audience="authenticated",
            options={"verify_exp": True}
        )

    def get_or_create_user(self, payload):
        supabase_uid = payload.get('sub')
        email = payload.get('email')
        
        # Metadata from Google/Auth providers
        user_metadata = payload.get('user_metadata', {})
        full_name = user_metadata.get('full_name') or user_metadata.get('name', '')

        if not supabase_uid:
            raise AuthenticationFailed('Token missing "sub" claim')

        try:
            user = User.objects.get(supabase_uid=supabase_uid)
            return (user, None)
        except User.DoesNotExist:
            pass

        try:
            user = User.objects.get(email=email)
            user.supabase_uid = supabase_uid
            user.save()
            return (user, None)
        except User.DoesNotExist:
            pass

        user = User.objects.create(
            supabase_uid=supabase_uid,
            email=email,
            username=email,  # Fallback: set username same as email
            first_name=full_name.split(' ')[0] if full_name else '',
            last_name=' '.join(full_name.split(' ')[1:]) if full_name else '',
            is_active=True
        )
        user.set_unusable_password()
        user.save()

        return (user, None)