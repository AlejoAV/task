import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from core.utils.jwt_auth import JWTAuthHandler

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_user(db):
    def make_user(**kwargs):
        if 'username' not in kwargs:
            kwargs['username'] = 'testuser'
        if 'password' not in kwargs:
            kwargs['password'] = 'testpass123'
        return User.objects.create_user(**kwargs)
    return make_user

@pytest.fixture
def auth_user_token(create_user):
    user = create_user()
    token, _ = Token.objects.get_or_create(user=user)
    # Generamos también un JWT válido para headers si fuera necesario simular entrada externa
    # Pero DRF TokenAuth usa "Token <key>".
    # El LoginWithJWT usa un custom header o lo que haya definido el user.
    # Mirando auth.py: credential_jwt = request.META.get('HTTP_AUTHORIZATION', 'NA')
    return {
        'user': user,
        'token': token,
        'headers': {'HTTP_AUTHORIZATION': f'Bearer {token.key}'} # Ajustar según necesidad real
    }

@pytest.fixture
def jwt_auth_headers(create_user):
    """
    Genera headers para autenticarse contra los endpoints que requieren TokenAuthentication
    o para el endpoint de login si requiere JWT previo (el login en auth.py decodifica un JWT).
    """
    user = create_user(username='jwtuser', password='jwtpassword')
    import jwt
    from django.conf import settings
    
    payload = {
        'username': 'jwtuser',
        'password': 'jwtpassword'
    }
    encoded_jwt = jwt.encode(payload, settings.JWT_TOKEN, algorithm='HS256')
    
    return {
        'user': user,
        'login_headers': {'HTTP_AUTHORIZATION': f'Bearer {encoded_jwt}'},
        'password': 'jwtpassword'
    }
