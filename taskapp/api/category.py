from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from core.view.api import BaseAPIResponse
from taskapp.models import CategoryModel
from taskapp.serializers.category import CategorySerializer

class PageCategoryResults(PageNumberPagination):
    page_size = 2


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = CategoryModel.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageCategoryResults
    renderer_classes = [BaseAPIResponse]