import pytest
from django.urls import reverse
from rest_framework import status
from taskapp.models import CategoryModel

@pytest.mark.django_db
class TestCategory:
    def test_create_category_authenticated(self, api_client, create_user):
        """
        Prueba crear una categoría estando autenticado.
        """
        user = create_user()
        api_client.force_authenticate(user=user)
        
        url = reverse('taskapp:categorymodel-list')
        data = {'name': 'Work', 'description': 'Work related stuff'}
        response = api_client.post(url, data)
        
        assert response.status_code == status.HTTP_201_CREATED
        # Verificamos que se creó uno nuevo con ese nombre, en vez de asumir count == 1 absoluto
        assert CategoryModel.objects.filter(name='Work').exists()

    def test_create_category_unauthenticated(self, api_client):
        """
        Prueba que falla al crear categoría sin autenticación.
        """
        url = reverse('taskapp:categorymodel-list')
        data = {'name': 'Personal'}
        response = api_client.post(url, data)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_categories(self, api_client, create_user):
        """
        Prueba listar categorías.
        """
        user = create_user()
        api_client.force_authenticate(user=user)
        
        CategoryModel.objects.create(name='Cat1', description='Desc1')
        CategoryModel.objects.create(name='Cat2', description='Desc2')
        
        url = reverse('taskapp:categorymodel-list')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        json_response = response.json()
        data_content = json_response['data']
        assert len(data_content) >= 5

    def test_retrieve_update_delete_category(self, api_client, create_user):
        """
        Prueba obtener, actualizar y borrar una categoría.
        """
        user = create_user()
        api_client.force_authenticate(user=user)
        
        category = CategoryModel.objects.create(name='Original', description='Original Desc')
        url_detail = reverse('taskapp:categorymodel-detail', args=[category.id])
        
        # Retrieve
        response = api_client.get(url_detail)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['data']['name'] == 'Original'
        
        # Update
        response = api_client.put(url_detail, {'name': 'Updated', 'description': 'Updated Desc'})
        assert response.status_code == status.HTTP_200_OK
        category.refresh_from_db()
        assert category.name == 'Updated'
        
        # Delete
        response = api_client.delete(url_detail)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not CategoryModel.objects.filter(id=category.id).exists()
