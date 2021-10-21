from rest_framework import serializers, status
from rest_framework.exceptions import NotFound
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from kite_runner.models import Profile, profile
from kite_runner.utils.constants import DEFAULT_AVT_IMAGE

from .renderer import ProfileJSONRenderer


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")
    bio = serializers.CharField(allow_blank=True, required=False)
    image = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ["username", "bio", "image", "following"]
        read_only_fields = ["username"]

    def get_image(self, obj):
        if obj.image:
            return obj.image

        return DEFAULT_AVT_IMAGE

    def get_following(self, instance):
        request = self.context.get("request")
        if request is None:
            return False
        if not request.user.is_authenticated:
            return False

        follower = request.user.profile
        followee = instance

        return follower.is_following(followee)


class ProfileRetrieveAPIView(RetrieveAPIView):
    permission_classes = (AllowAny,)
    queryset = Profile.objects.select_related("user")
    serializer_class = ProfileSerializer
    renderer_classes = (ProfileJSONRenderer,)

    def retrieve(self, request, username):
        try:
            profile: Profile = self.queryset.get(user__username=username)
        except Profile.DoesNotExist:
            raise NotFound(f"Profile with username: {username} not found.")

        serializer = self.serializer_class(profile, context={"request": request})

        return Response(serializer.data, status=status.HTTP_200_OK)


class FollowUserAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    queryset = Profile.objects.select_related("user")
    serializer_class = ProfileSerializer
    renderer_classes = (ProfileJSONRenderer,)

    def post(self, request, username):

        follower: Profile = self.request.user.profile
        try:
            followee: Profile = self.queryset.get(user__username=username)
        except Profile.DoesNotExist:
            raise NotFound(f"Profile with username: {username} not found.")

        follower.follow(followee)

        serializer = self.serializer_class(followee, context={"request": request})

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, username):
        user = request.user
        followee_profile = Profile.objects.get(user__username=username)
        user.profile.unfollow(followee_profile)

        return Response(status=status.HTTP_200_OK)
