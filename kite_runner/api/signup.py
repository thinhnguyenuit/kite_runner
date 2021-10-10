from django.contrib.auth import password_validation
from rest_framework import permissions, serializers, status, validators
from rest_framework.response import Response
from rest_framework.views import APIView

from kite_runner.models.user import User

from .renderer import UserJSONRenderer


class SignupSerializer(serializers.Serializer):
    username: serializers.Field = serializers.CharField(
        max_length=100,
        validators=[
            validators.UniqueValidator(
                queryset=User.objects.all(), message="Username already exists"
            )
        ],
    )
    email: serializers.Field = serializers.EmailField(
        validators=[
            validators.UniqueValidator(
                queryset=User.objects.all(),
                message="User with this email already exists",
            )
        ]
    )
    password: serializers.Field = serializers.CharField(min_length=6)

    def validate_password(self, value):
        if value is not None:
            password_validation.validate_password(value)
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class SignupAPIView(APIView):
    serializer_class = SignupSerializer
    permission_classes = (permissions.AllowAny,)
    renderer_classes = (UserJSONRenderer,)

    def post(self, request):
        user = request.data.get("user", {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
