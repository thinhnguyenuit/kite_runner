from rest_framework import serializers

from kite_runner.models import Profile


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

        return "https://www.gravatar.com/avatar/73af357c60e22857eda9a5dbf106e2f0"

    def get_following(self, instance):
        request = self.context.get("request")
        if request is None:
            return False
        if not request.user.is_authenticated():
            return False

        follower = request.user.profile
        followee = instance

        return follower.is_following(followee)
