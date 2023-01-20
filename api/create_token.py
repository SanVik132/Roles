from functools import partial
from api.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.backends import TokenBackend

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh)

def get_user_from_token(token):
    try:
        valid_data = TokenBackend(algorithm='HS256').decode(str(token),verify=False)
        user = valid_data
        user_id = user['user_id']
        try:
            user = User.objects.get(pk =user_id )
            return user
        except:
            return 0
    except:
        return 0