from rest_framework import status

from kite_runner.models import Article, Comment
from kite_runner.utils.constants import TOKEN_HEADER
from kite_runner.utils.tokens import get_user_token

from .base import APIBaseTest


class TestCommentAPIView(APIBaseTest):
    def setUp(self) -> None:
        super().setUp()
        self.article: Article = Article.objects.create(
            title="Test Article",
            body="Test Body",
            description="Test Description",
            author=self.user.profile,
        )
        self.comment: Comment = Comment.objects.create(
            body="Test Comment", article=self.article, author=self.user.profile
        )
        self.token = get_user_token(self.user)

    def test_get_all_comments_for_article(self) -> None:
        response = self.client.get(f"/api/v1/articles/{self.article.slug}/comments/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()
        self.assertIsNotNone(response_data)
        self.assertEqual(response_data["count"], 1)
        self.assertEqual(response_data["comments"][0]["body"], self.comment.body)
        self.assertIsNotNone(response_data["comments"][0]["author"])
        self.assertIsNotNone(response_data["comments"][0]["createdAt"])
        self.assertIsNotNone(response_data["comments"][0]["updatedAt"])

    def test_get_all_comments_for_article_no_articles_found(self) -> None:
        response = self.client.get("/api/v1/articles/invalid-slug/comments/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["count"], 0)

    def test_create_comment_for_article(self) -> None:
        response = self.client.post(
            f"/api/v1/articles/{self.article.slug}/comments/",
            {"comment": {"body": "New Comment"}},
            HTTP_AUTHORIZATION=TOKEN_HEADER.format(self.token),
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response_data = response.json()["comment"]
        self.assertIsNotNone(response_data)
        self.assertEqual(response_data["body"], "New Comment")
        self.assertIsNotNone(response_data["author"])
        self.assertIsNotNone(response_data["createdAt"])
        self.assertIsNotNone(response_data["updatedAt"])
