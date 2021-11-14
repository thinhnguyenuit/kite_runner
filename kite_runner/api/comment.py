from typing import Any, Dict

from django.db.models import QuerySet
from rest_framework import generics, serializers, status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from kite_runner.api.profile import ProfileSerializer
from kite_runner.api.renderer import CommentJSONRenderer
from kite_runner.models import Article, Comment


class CommentSerializer(serializers.ModelSerializer):
    author = ProfileSerializer(required=False)
    createdAt = serializers.SerializerMethodField(method_name="get_created_at")
    updatedAt = serializers.SerializerMethodField(method_name="get_updated_at")

    class Meta:
        model = Comment
        fields = (
            "id",
            "author",
            "body",
            "createdAt",
            "updatedAt",
        )

    def create(self, validated_data: Dict) -> Comment:
        article = self.context["article"]
        author = self.context["author"]

        return Comment.objects.create(article=article, author=author, **validated_data)

    def get_created_at(self, obj: Comment) -> str:
        return obj.created_at.isoformat()

    def get_updated_at(self, obj: Comment) -> str:
        return obj.updated_at.isoformat()


class CommentListCreateAPIView(generics.ListCreateAPIView):
    lookup_field = "article__slug"
    lookup_url_kwarg = "article_slug"
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Comment.objects.select_related(
        "article", "article__author", "article__author__user", "author", "author__user"
    )
    renderer_classes = (CommentJSONRenderer,)
    serializer_class = CommentSerializer

    def filter_queryset(self, queryset: QuerySet) -> QuerySet:
        filters = {self.lookup_field: self.kwargs[self.lookup_url_kwarg]}

        return queryset.filter(**filters)

    def create(self, request: Any, article_slug: str) -> Response:
        data = request.data.get("comment", {})
        context = {"author": request.user.profile}

        try:
            context["article"] = Article.objects.get(slug=article_slug)
        except Article.DoesNotExist:
            return NotFound(f"Could not found any article with slug: {article_slug}")

        serializer = self.serializer_class(data=data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CommentDestroyAPIView(generics.DestroyAPIView):
    lookup_url_kwarg = "comment_pk"
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Comment.objects.all()

    def destroy(self, comment_pk: Any) -> Response:
        try:
            comment = Comment.objects.get(pk=comment_pk)
        except Comment.DoesNotExist:
            return NotFound(f"Could not found any comment with pk: {comment_pk}")

        comment.delete()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
