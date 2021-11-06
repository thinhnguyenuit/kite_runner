from typing import Any, Dict

from django.contrib.auth import authenticate
from rest_framework import permissions, serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from kite_runner.utils import tokens

from .renderer import UserJSONRenderer


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField(max_length=False, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        fields = ("email", "username", "password", "token")

    def to_representation(self, value: Any) -> Any:
        return value

    def validate(self, data: Dict) -> Dict:
        email = data.get("email", None)
        password = data.get("password", None)

        if not email or not password:
            raise serializers.ValidationError("Email and password are required")

        user = authenticate(email=email, password=password)

        if user is None:
            raise serializers.ValidationError("wrong username or password")

        return {
            "email": user.email,
            "username": user.username,
            "token": tokens.get_user_token(user),
        }


class LoginViewSet(APIView):
    serializer_class = LoginSerializer
    permission_classes = (permissions.AllowAny,)
    renderer_classes = (UserJSONRenderer,)

    def post(self, request: Any) -> Response:
        user = request.data.get("user", None)

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
