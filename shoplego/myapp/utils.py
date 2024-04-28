# utils.py

from datetime import datetime, timedelta
from rest_framework_simplejwt.tokens import AccessToken

class CustomPayload(AccessToken):
    @classmethod
    def for_user(cls, user):
        token = cls()
        token['id_user'] = user.id_user  # Use id_user instead of id
        token['exp'] = datetime.now() + timedelta(days=3)
        return token
