import pytest
from django.urls import reverse
from rest_framework import status
from taskapp.models import TaskModel, CategoryModel

@pytest.mark.django_db
class TestTask:
    def test_create_task(self, api_client, create_user):
        """
        Prueba crear una tarea. Verifica que se asigne usuario y color.
        """
        user = create_user()
        api_client.force_authenticate(user=user)
        
        url = reverse('taskapp:taskmodel-list')
        data = {'name': 'My Task', 'status': 'TODO'}
        response = api_client.post(url, data)
        
        assert response.status_code == status.HTTP_201_CREATED
        json_response = response.json()
        task_id = json_response['data']['id']
        
        task = TaskModel.objects.get(pk=task_id)
        assert task.name == 'My Task'
        assert task.user == user
        assert task.color is not None # Se genera random
        
    def test_list_tasks_only_user(self, api_client, create_user):
        """
        Prueba que un usuario solo vea sus propias tareas.
        """
        user1 = create_user(username='u1')
        user2 = create_user(username='u2')
        
        TaskModel.objects.create(name='Task U1', user=user1)
        TaskModel.objects.create(name='Task U2', user=user2)
        
        api_client.force_authenticate(user=user1)
        url = reverse('taskapp:taskmodel-list')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        json_response = response.json()
        tasks_data = json_response['data']
        if 'results' in tasks_data:
            results = tasks_data['results']
        else:
            results = tasks_data
            
        assert len(results) == 1
        assert results[0]['name'] == 'Task U1'

    def test_update_status(self, api_client, create_user):
        """
        Prueba actualizar el estado de una tarea.
        """
        user = create_user()
        api_client.force_authenticate(user=user)
        
        task = TaskModel.objects.create(name='Task', user=user, status='TODO')
        url = reverse('taskapp:taskmodel-detail', args=[task.id])
        
        response = api_client.patch(url, {'status': 'DONE'})
        assert response.status_code == status.HTTP_200_OK
        
        task.refresh_from_db()
        assert task.status == 'DONE'

    def test_delete_task(self, api_client, create_user):
        """
        Prueba borrar una tarea.
        """
        user = create_user()
        api_client.force_authenticate(user=user)
        
        task = TaskModel.objects.create(name='Task to delete', user=user)
        url = reverse('taskapp:taskmodel-detail', args=[task.id])
        
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert TaskModel.objects.count() == 0
