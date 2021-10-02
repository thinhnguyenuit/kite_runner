from django.contrib.auth import password_validation
from rest_framework import generics, permissions, serializers, validators

from kite_runner.models.user import User


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


class SignupViewSet(generics.CreateAPIView):
    serializer_class = SignupSerializer
    permission_classes = (permissions.AllowAny,)
