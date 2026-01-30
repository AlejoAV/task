from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from core.view.api import BaseAPIResponse
from taskapp.serializers.auth import LoginSerializer
from drf_spectacular.utils import extend_schema


class LoginWithJWT(APIView):
    permission_classes = []
    renderer_classes = [BaseAPIResponse]

    @extend_schema(request=LoginSerializer, responses=None)
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"error": "Datos inválidos", "details": serializer.errors}, status=400)
            
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user = authenticate(username=username, password=password)

        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "api_token": token.key,
                "user": user.username,
                "created": created
            })

        return Response({"error": "Credenciales incorrectas"}, status=400)


class LogoutView(APIView):
    renderer_classes = [BaseAPIResponse, ]

    def post(self, request):
        request.user.auth_token.delete()
        return Response({"message": "Token eliminado con éxito"}, status=200)