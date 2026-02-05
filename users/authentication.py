import jwt
import base64
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
from django.contrib.auth import get_user_model
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend

User = get_user_model()

class SupabaseAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None

        try:
            parts = auth_header.split()
            if len(parts) != 2 or parts[0].lower() != 'bearer':
                raise AuthenticationFailed('Authorization header must be "Bearer <token>"')
            
            token = parts[1]
            
            # Step 1: Verify the token locally (No network call)
            payload = self.verify_token_locally(token)
            
            # Step 2: Sync with Django User model
            return self.get_or_create_user(payload)

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token expired.")
        except Exception as e:
            raise AuthenticationFailed(f"Auth failed: {str(e)}")

    def verify_token_locally(self, token):
        import base64
        from cryptography.hazmat.primitives.asymmetric import ec
        from cryptography.hazmat.backends import default_backend

        # These are the EXACT coordinates you just provided
        x_str = "J46soCb0LMKLVf_QHyWEKR0w5bB82PShdZdHQrIJf6c"
        y_str = "FcZ3z3f3uHg6vYV_vaQ92-jS4SPo7TxlJyEtLjwS5TU"

        def b64_decode(data):
            # Supabase/JWT uses base64url encoding. We must add padding if needed.
            rem = len(data) % 4
            if rem > 0:
                data += "=" * (4 - rem)
            return base64.urlsafe_b64decode(data)

        try:
            # 1. Decode the coordinates into bytes
            x_bytes = b64_decode(x_str)
            y_bytes = b64_decode(y_str)

            # 2. Reconstruct the Public Key from your project's P-256 curve
            public_key = ec.EllipticCurvePublicNumbers(
                int.from_bytes(x_bytes, 'big'),
                int.from_bytes(y_bytes, 'big'),
                ec.SECP256R1()
            ).public_key(default_backend())

            # 3. Verify the token signature
            return jwt.decode(
                token,
                public_key,
                algorithms=["ES256"],
                audience="authenticated",
                options={
                    "verify_exp": True,
                    "leeway": 60
                }
            )
        except Exception as e:
            raise Exception(f"Signature check failed: {str(e)}")
        
    def get_or_create_user(self, payload):
        supabase_uid = payload.get('sub')
        email = payload.get('email')
        
        if not supabase_uid:
            raise AuthenticationFailed('Invalid payload: missing sub')

        # 1. Search by id (which is your supabase_id)
        user = User.objects.filter(id=supabase_uid).first()
        if user:
            return (user, None)

        # 2. Search by email to prevent duplicate accounts if the ID is different
        user = User.objects.filter(email=email).first()
        if user:
            # Optional: Link the ID if it wasn't linked already
            user.id = supabase_uid
            user.save()
            return (user, None)

        # 3. Create new user if not found
        try:
            user = User.objects.create(
                id=supabase_uid,
                email=email,
                username=email,
                is_active=True,
                # Fix: If your model requires a phone_number but it's unique,
                # we set it to None (NULL) so the DB doesn't complain about 
                # multiple empty strings "".
                phone_number=None 
            )
            user.set_unusable_password()
            user.save()
            return (user, None)
        except Exception as e:
            raise AuthenticationFailed(f"Database error during user creation: {str(e)}")