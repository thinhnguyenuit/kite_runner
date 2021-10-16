from django.contrib.auth import password_validation
from rest_framework import permissions, serializers, status, validators
from rest_framework.response import Response
from rest_framework.views import APIView

from kite_runner.models import User
from kite_runner.api.profile import ProfileSerializer

from .renderer import UserJSONRenderer
from kite_runner.utils import tokens


class SignupSerializer(serializers.ModelSerializer):
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
    password: serializers.Field = serializers.CharField(min_length=6, write_only=True)
    token = serializers.SerializerMethodField(required=False)
    profile = ProfileSerializer(write_only=True, required=False)
    bio = serializers.CharField(source="profile.bio", read_only=True, required=False)
    image = serializers.URLField(source="profile.image", read_only=True, required=False)

    class Meta:
        model = User
        fields = ("email", "token", "username", "password", "profile", "bio", "image")
        extra_kwargs = {
            "password": {"write_only": True},
            "token": {"read_only": True},
        }

    def validate_password(self, value):
        if value is not None:
            password_validation.validate_password(value)
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def get_token(self, user):
        return tokens.get_user_token(user)


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
