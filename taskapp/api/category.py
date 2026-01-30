from rest_framework import viewsets

from core.view.api import BaseAPIResponse
from taskapp.models import CategoryModel
from taskapp.serializers.category import CategorySerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = CategoryModel.objects.all()
    serializer_class = CategorySerializer
    renderer_classes = [BaseAPIResponse]