from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters as drf_filters
from rest_framework.pagination import PageNumberPagination

from taskapp.filters.task import TaskFilter
from taskapp.models import TaskModel
from taskapp.serializers.task import TaskSerializer

class TaskCategoryResults(PageNumberPagination):
    page_size = 6

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    queryset = TaskModel.objects.all()
    filter_backends = [TaskFilter, drf_filters.OrderingFilter]
    search_fields = ['status__icontains',]
    ordering = '-id'
    pagination_class = TaskCategoryResults
