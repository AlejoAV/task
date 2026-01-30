import pytest
from django.urls import reverse
from rest_framework import status

@pytest.mark.django_db
class TestAuth:
    def test_login_success(self, api_client, jwt_auth_headers):
        """
        Prueba que el login con un JWT válido (que contiene user/pass) retorna un token de API.
        """
        url = reverse('taskapp:login')
        response = api_client.post(url, **jwt_auth_headers['login_headers'])
        
        json_response = response.json()
        assert response.status_code == 200
        assert json_response['status'] == 'success'
        assert 'api_token' in json_response['data']
        assert json_response['data']['user'] == jwt_auth_headers['user'].username

    def test_login_failure_invalid_jwt(self, api_client):
        """
        Prueba que falla si el JWT es inválido o no existe.
        """
        url = reverse('taskapp:login')
        response = api_client.post(url, HTTP_AUTHORIZATION='Bearer invalidtoken')
        
        json_response = response.json()
        assert response.status_code == 400
        assert json_response['status'] == 'error'

    def test_login_failure_wrong_credentials(self, api_client):
        """
        Prueba que falla si el JWT es válido pero las credenciales dentro son incorrectas (usuario inexistente).
        """
        import jwt
        from django.conf import settings
        
        payload = {'username': 'wronguser', 'password': 'wrongpass'}
        encoded_jwt = jwt.encode(payload, settings.JWT_TOKEN, algorithm='HS256')
        
        url = reverse('taskapp:login')
        response = api_client.post(url, HTTP_AUTHORIZATION=f'Bearer {encoded_jwt}')
        
        json_response = response.json()
        assert response.status_code == 401
        assert json_response['status'] == 'error'

    def test_logout(self, api_client, create_user):
        """
        Prueba el logout eliminando el token.
        """
        user = create_user()
        from rest_framework.authtoken.models import Token
        token, _ = Token.objects.get_or_create(user=user)
        
        url = reverse('taskapp:logout')
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = api_client.post(url)
        
        assert response.status_code == 200
        assert not Token.objects.filter(user=user).exists()
