from rest_framework import status

from kite_runner.models import Article
from kite_runner.utils.constants import TOKEN_HEADER

from .base import APIBaseTest


class TestArticleViewset(APIBaseTest):

    article_url = "/api/v1/articles"
    article_title = "How to train your dragon"
    article_description = "Ever wonder how?"
    article_body = "Very carefully."
    article_tag_list = ["training", "dragons"]
    article_data = {
        "article": {
            "title": article_title,
            "description": article_description,
            "body": article_body,
            "tagList": article_tag_list,
        }
    }

    @classmethod
    def setUpTestData(cls):
        super().setup_test_data()  # type: ignore

    def test_create_article(self) -> None:
        response = self.client.post(
            f"{self.article_url}/",
            data=self.article_data,
            HTTP_AUTHORIZATION=TOKEN_HEADER.format(self.token[0].key),
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)\

        response_data = response.json()
        self.assertIsNotNone(response_data)

        article_data = response_data["article"]
        self.assertIsNotNone(article_data)
        self.assertIsNotNone(article_data["slug"])
        self.assertEqual(article_data["title"], self.article_title)
        self.assertEqual(article_data["description"], self.article_description)
        self.assertEqual(article_data["body"], self.article_body)
        self.assertEqual(article_data["tagList"], self.article_tag_list)
        self.assertIsNotNone(article_data["createdAt"])
        self.assertEqual(article_data["author"]["username"], self.user.username)
        self.assertEqual(article_data["favorited"], False)
        self.assertEqual(article_data["favoritesCount"], 0)

    def test_create_article_with_invalid_data(self) -> None:
        response = self.client.post(
            f"{self.article_url}/",
            data={"article": {"title": self.article_title}},
            HTTP_AUTHORIZATION=TOKEN_HEADER.format(self.token[0].key),
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_article_with_invalid_token(self):
        response = self.client.post(
            f"{self.article_url}/",
            data=self.article_data,
            HTTP_AUTHORIZATION=TOKEN_HEADER.format("invalid_token"),
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_article_without_token(self):
        response = self.client.post(f"{self.article_url}/", data=self.article_data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json(), self.unauthenticated_response())

    def test_get_article(self):
        """
        test get recent articles globally
        """

        Article.objects.create(
            title=self.article_title,
            author=self.user,
            description=self.article_description,
            body=self.article_body,
            tag_list=self.article_tag_list,
        )

        response = self.client.get(
            f"{self.article_url}",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()
        self.assertIsNotNone(response_data)
        self.assertEqual(response_data["articles"][0]["title"], self.article_title)
        self.assertEqual(
            response_data["articles"][0]["description"], self.article_description
        )
        self.assertEqual(response_data["articles"][0]["body"], self.article_body)
        self.assertEqual(response_data["articles"][0]["tags"], self.article_tag_list)
        self.assertEqual(
            response_data["articles"][0]["author"]["username"], "test_user"
        )
