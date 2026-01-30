import pytest
from django.urls import reverse
from rest_framework import status

@pytest.mark.django_db
class TestAuth:
    def test_login_success(self, api_client, jwt_auth_headers):
        # Prueba que el login con credenciales válidas retorna token
        url = reverse('taskapp:login')
        data = {
            'username': jwt_auth_headers['user'].username,
            # 'jwt_auth_headers' usa 'jwtpassword' como password por defecto en conftest.py
            'password': jwt_auth_headers['password'] 
        }
        
        response = api_client.post(url, data, format='json')
        
        json_response = response.json()
        assert response.status_code == 200
        assert json_response['status'] == 'success'
        assert 'api_token' in json_response['data']
        assert json_response['data']['user'] == jwt_auth_headers['user'].username

    def test_login_failure_invalid_data(self, api_client):
        """
        Prueba que falla si faltan datos
        """
        url = reverse('taskapp:login')
        response = api_client.post(url, {'username': 'solo'}, format='json')
        
        json_response = response.json()
        assert response.status_code == 400
        assert json_response['status'] == 'error'

    def test_login_failure_wrong_credentials(self, api_client):
        """
        Prueba credenciales incorrectas
        """
        url = reverse('taskapp:login')
        data = {'username': 'wrong', 'password': 'wrong'}
        response = api_client.post(url, data, format='json')
        
        json_response = response.json()
        # Status code 400 segun nueva implementacion, o 401 si asi lo decidimos.
        # En el view puse return Response(..., status=400) para credenciales incorrectas.
        assert response.status_code == 400 
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
