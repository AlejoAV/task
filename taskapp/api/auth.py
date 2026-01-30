from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from core.utils.jwt_auth import JWTAuthHandler
from core.view.api import BaseAPIResponse


class LoginWithJWT(APIView):
    permission_classes = []
    renderer_classes = [BaseAPIResponse]

    def post(self, request):
        credential_jwt = request.META.get('HTTP_AUTHORIZATION', 'NA')
        payload = JWTAuthHandler.decode_any_token(credential_jwt)

        if not payload or 'username' not in payload or 'password' not in payload:
            return Response({"error": "JWT de credenciales inválido"}, status=400)

        user = authenticate(username=payload['username'], password=payload['password'])

        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "api_token": token.key,
                "user": user.username,
                "created": created
            })

        return Response({"error": "Credenciales incorrectas"}, status=401)


class LogoutView(APIView):
    renderer_classes = [BaseAPIResponse, ]

    def post(self, request):
        request.user.auth_token.delete()
        return Response({"message": "Token eliminado con éxito"}, status=200)