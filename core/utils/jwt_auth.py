import jwt
from datetime import datetime, timedelta, timezone
from django.conf import settings

class JWTAuthHandler:
    @staticmethod
    def create_access_token(user_id):
        """Genera el token para usar las APIs"""
        payload = {
            'user_id': user_id,
            'type': 'access',
            'exp': datetime.now(timezone.utc) + timedelta(hours=8)
        }
        return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

    @staticmethod
    def decode_any_token(token):
        try:
            token = token.split('Bearer ')[-1]
            return jwt.decode(token, settings.JWT_TOKEN, algorithms=['HS256'])
        except Exception:
            return None