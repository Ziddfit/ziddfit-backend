from rest_framework_simplejwt.tokens import RefreshToken 


def get_refresh_token(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh' : str(refresh),
        'access' : str(refresh.access_token),
    }

def get_user_role(user):
    if hasattr(user,'gym_profile'):
        return 'member'
    elif hasattr(user,'owner'):
        return 'owner'
    elif hasattr(user,'staff_profile'):
        return 'staff'
    return None