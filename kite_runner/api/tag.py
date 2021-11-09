from typing import Any
from kite_runner.models import Tag
from rest_framework import serializers, generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("tag",)

    def to_representation(self, obj: Any) -> Tag:
        return obj.tag


class TagListAPIView(generics.ListAPIView):
    queryset = Tag.objects.all()
    permission_classes = (AllowAny,)
    pagination_class = None
    serializer_class = TagSerializer

    def list(self, request: Any) -> Response:
        serializer_data = self.get_queryset()
        serializer = self.serializer_class(serializer_data, many=True)

        return Response({"tags": serializer.data}, status=status.HTTP_200_OK)
