from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access':  str(refresh.access_token),
    }


def get_user_role(user):
    if hasattr(user, 'owner'):
        return 'owner'
    if hasattr(user, 'staff'):
        return 'staff'
    return 'member'