from django.urls import include, path
from rest_framework import routers

from taskapp.api.category import CategoryViewSet
from taskapp.api.task import TaskViewSet

router = routers.DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'tasks', TaskViewSet)

app_name = "taskapp"

urlpatterns = [
    path('', include(router.urls)),
]