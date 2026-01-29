from django.urls import include, path
from rest_framework import routers

from taskapp.api.category import CategoryViewSet

router = routers.DefaultRouter()
router.register(r'categories', CategoryViewSet)

app_name = "taskapp"

urlpatterns = [
    path('', include(router.urls)),
]