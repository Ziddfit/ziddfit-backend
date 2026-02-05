# app_name/authentication.py

import jwt
from jwt import PyJWKClient
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

class SupabaseAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # 1. Extract the Authorization header
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None # Pass to next auth class (or fail if none)

        try:
            # Format: "Bearer <token>"
            prefix, token = auth_header.split()
            if prefix.lower() != 'bearer':
                raise AuthenticationFailed('Authorization header must start with Bearer')
        except ValueError:
            raise AuthenticationFailed('Invalid Authorization header format')

        # 2. Verify the JWT
        payload = self._decode_jwt(token)

        # 3. Get or Create the Django User
        return self._get_or_create_user(payload)

    def _decode_jwt(self, token):
        # Fetch Supabase's public keys (JWKS)
        jwks_url = f"{settings.SUPABASE_URL}/auth/v1/keys"
        jwks_client = PyJWKClient(jwks_url)

        try:
            # Get the signing key from the token header
            signing_key = jwks_client.get_signing_key_from_jwt(token)

            # Verify signature, expiration, and audience
            payload = jwt.decode(
                token,
                signing_key.key,
                algorithms=["RS256"],
                audience=settings.SUPABASE_JWT_AUDIENCE,
                options={"verify_exp": True}
            )
            return payload
        except jwt.PyJWTError as e:
            raise AuthenticationFailed(f"Token validation failed: {str(e)}")

    def _get_or_create_user(self, payload):
        supabase_uid = payload.get('sub')
        email = payload.get('email')

        if not supabase_uid:
            raise AuthenticationFailed('Token missing "sub" (User ID) claim')

        try:
            # 1. Try to find the user by Supabase ID
            user = User.objects.get(supabase_uid=supabase_uid)
        except User.DoesNotExist:
            # 2. If not found, create a new User
            # Extract metadata (Google SSO usually sends name in user_metadata)
            user_metadata = payload.get('user_metadata', {})
            full_name = user_metadata.get('full_name', '') or user_metadata.get('name', '')

            # Create the user without a password (since Supabase handles it)
            user = User.objects.create(
                supabase_uid=supabase_uid,
                email=email,
                username=email,  # Using email as username
                full_name=full_name,
                is_active=True
            )
            user.set_unusable_password()
            user.save()

        return (user, None) # DRF requires (user, auth) tuples