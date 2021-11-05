from typing import Any, Dict, Optional

from django.db.models import QuerySet
from rest_framework import mixins, serializers, status, viewsets
from rest_framework.exceptions import NotAuthenticated, NotFound
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from kite_runner.api.renderer import ArticleJSONRenderer
from kite_runner.models import Article, Tag

from .profile import ProfileSerializer


class TagRelatedField(serializers.RelatedField):
    def get_queryset(self) -> QuerySet:
        return Tag.objects.all()

    def to_internal_value(self, data: Any) -> Tag:
        tag, _ = Tag.objects.get_or_create(tag=data, slug=data.lower())
        return tag

    def to_representation(self, value: Tag) -> str:
        return value.tag


class ArticleSerializer(serializers.ModelSerializer):
    author = ProfileSerializer(read_only=True)
    description = serializers.CharField(required=False)
    slug = serializers.SlugField(required=False)
    favorited = serializers.SerializerMethodField()
    tagList = TagRelatedField(many=True, required=False, source="tags")
    createdAt = serializers.SerializerMethodField(method_name="get_created_at")
    updatedAt = serializers.SerializerMethodField(method_name="get_updated_at")
    favoritesCount = serializers.SerializerMethodField(
        method_name="get_fovorties_count"
    )

    class Meta:
        model = Article
        fields = (
            "slug",
            "title",
            "description",
            "body",
            "tagList",
            "createdAt",
            "updatedAt",
            "favorited",
            "favoritesCount",
            "author",
        )

    def create(self, validated_data: Dict) -> Article:
        author = self.context.get("author", None)
        tags = validated_data.pop("tags", [])
        article: Article = Article.objects.create(author=author, **validated_data)

        for tag in tags:
            article.tags.add(tag)

        return article

    def get_favorited(self, instance: Any) -> bool:
        request = self.context.get("request", None)
        if not request:
            return False

        if not request.user.is_authenticated:
            return False

        return request.user.profile.has_favorited(instance)

    def get_created_at(self, instance: Any) -> str:
        return instance.created_at.isoformat()

    def get_updated_at(self, instance: Any) -> str:
        return instance.updated_at.isoformat()

    def get_fovorties_count(self, instance: Any) -> int:
        return instance.favorited_by.count()


class ArticleViewset(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    lookup_field = "slug"
    queryset = Article.objects.select_related("author", "author__user")
    permissions_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = ArticleSerializer
    renderer_classes = (ArticleJSONRenderer,)

    def get_queryset(self) -> QuerySet:
        queryset: QuerySet = self.queryset

        author = self.request.query_params.get("author", None)
        if author:
            queryset = queryset.filter(author__user__username=author)

        tag = self.request.query_params.get("tag", None)
        if tag:
            queryset = queryset.filter(tags__tag=tag)

        favorited_by = self.request.query_params.get("favorited", None)
        if favorited_by:
            queryset = queryset.filter(favorited_by__username=favorited_by)

        return queryset

    def create(self, request: Any) -> Response:
        if not request.user.is_authenticated:
            raise NotAuthenticated("Authentication credentials were not provided.")
        serializer_context = {"author": request.user.profile, "request": request}
        serializer_data = request.data.get("article", {})

        serializer: ArticleSerializer = self.serializer_class(
            data=serializer_data, context=serializer_context
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request: Any) -> Response:
        serializer_context = {"request": request}
        page = self.paginate_queryset(self.get_queryset())

        serializer: ArticleSerializer = self.serializer_class(
            page, context=serializer_context, many=True
        )
        return self.get_paginated_response(serializer.data)

    def retrieve(self, request: Any, slug: Optional[str] = None) -> Response:
        serializer_context = {"request": request}
        try:
            instance = self.queryset.get(slug=slug)
        except Article.DoesNotExist:
            raise NotFound(f"Could not found any article with slug: {slug}")

        serializer = self.serializer_class(instance, context=serializer_context)

        return Response(serializer.data, status=status.HTTP_200_OK)
