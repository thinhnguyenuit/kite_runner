from rest_framework import serializers, status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from kite_runner.api.profile import ProfileSerializer
from kite_runner.models import User
from kite_runner.utils import tokens

from .renderer import UserJSONRenderer


class UserSerializer(serializers.ModelSerializer):

    token = serializers.SerializerMethodField()
    profile = ProfileSerializer(write_only=True)
    bio = serializers.CharField(source="profile.bio", read_only=True)
    image = serializers.URLField(source="profile.image", read_only=True)

    class Meta:
        model = User
        fields = ["email", "token", "username", "bio", "image", "profile"]
        read_only_fields = ("token",)

    def get_token(self, obj: "User") -> str:
        return tokens.get_user_token(obj)

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        profile_data = validated_data.pop("profile", {})

        for key, value in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)

        instance.save()

        for key, value in profile_data.items():
            setattr(instance.profile, key, value)

        instance.profile.save()

        return instance


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)

    def retrieve(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        user_data = request.data

        serializer_data = {
            "username": user_data.get("username", request.user.username),
            "email": user_data.get("email", request.user.email),
            "profile": {
                "bio": user_data.get("bio", request.user.profile.bio),
                "image": user_data.get("image", request.user.profile.image),
            },
        }

        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
