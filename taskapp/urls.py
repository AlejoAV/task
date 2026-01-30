from django.urls import include, path
from rest_framework import routers
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from taskapp.api.auth import LoginWithJWT, LogoutView
from taskapp.api.category import CategoryViewSet
from taskapp.api.task import TaskViewSet

router = routers.DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'tasks', TaskViewSet)

app_name = "taskapp"

urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginWithJWT.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    # Swagger Documentation
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='taskapp:schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='taskapp:schema'), name='redoc'),
]