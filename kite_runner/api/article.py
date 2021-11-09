from typing import Any, Dict

from django.db.models import Q, QuerySet
from rest_framework import generics, mixins, serializers, status, viewsets
from rest_framework.exceptions import NotAuthenticated, NotFound
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from kite_runner.api.renderer import ArticleJSONRenderer
from kite_runner.models import Article, Profile, Tag

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

    def retrieve(self, request: Any, slug: str) -> Response:
        serializer_context = {"request": request}
        try:
            instance = self.queryset.get(slug=slug)
        except Article.DoesNotExist:
            raise NotFound(f"Could not found any article with slug: {slug}")

        serializer = self.serializer_class(instance, context=serializer_context)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request: Any, slug: str) -> Response:
        serializer_context = {"request": request}

        try:
            instance = self.queryset.get(slug=slug)
        except Article.DoesNotExist:
            raise NotFound(f"Could not found any article with slug: {slug}")

        serializer_data = request.data.get("article", {})

        serializer = self.serializer_class(
            instance, context=serializer_context, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class ArticlesFavoriteAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (ArticleJSONRenderer,)
    serializer_class = ArticleSerializer

    def delete(self, request: Any, slug: str) -> Response:
        profile: Profile = self.request.user.profile
        serializer_context = {"request": request}

        try:
            article: Article = Article.objects.get(slug=slug)
        except Article.DoesNotExist:
            raise NotFound(f"Could not found any article with slug: {slug}")

        profile.unfavorite(article)
        serializer = self.serializer_class(article, context=serializer_context)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Any, slug: str) -> Response:
        profile: Profile = self.request.user.profile
        serializer_context = {"request": request}

        try:
            article: Article = Article.objects.get(slug=slug)
        except Article.DoesNotExist:
            raise NotFound(f"Could not found any article with slug: {slug}")

        profile.favorite(article)
        serializer = self.serializer_class(article, context=serializer_context)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ArticlesFeedAPIView(generics.ListAPIView):
    queryset = Article.objects.all()
    permission_classes = (IsAuthenticated,)
    renderer_classes = (ArticleJSONRenderer,)
    serializer_class = ArticleSerializer

    def get_queryset(self) -> QuerySet:
        return Article.objects.filter(
            Q(author__in=self.request.user.profile.following.all())
            | Q(author=self.request.user.profile)
        )

    def list(self, request: Any) -> Response:
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)

        serlizer_context = {"request": request}
        serializer = self.serializer_class(page, context=serlizer_context, many=True)
        return self.get_paginated_response(serializer.data)
