from rest_framework import status

from kite_runner.models import Article, Tag
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

    def test_create_article(self) -> None:
        response = self.client.post(
            f"{self.article_url}",
            data=self.article_data,
            HTTP_AUTHORIZATION=TOKEN_HEADER.format(self.token[0].key),
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
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
            f"{self.article_url}",
            data={"article": {"title": self.article_title}},
            HTTP_AUTHORIZATION=TOKEN_HEADER.format(self.token[0].key),
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_article_with_invalid_token(self):
        response = self.client.post(
            f"{self.article_url}",
            data=self.article_data,
            HTTP_AUTHORIZATION=TOKEN_HEADER.format("invalid_token"),
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_article_without_token(self):
        response = self.client.post(f"{self.article_url}", data=self.article_data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json(), self.unauthenticated_response())

    def test_get_article(self):
        """
        test get recent articles globally
        """

        article: Article = Article.objects.create(
            title=self.article_title,
            author=self.user.profile,
            description=self.article_description,
            body=self.article_body,
        )

        tag = Tag.objects.create(tag="training")
        article.tags.set([tag])

        response = self.client.get(
            f"{self.article_url}",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()
        self.assertIsNotNone(response_data)
        self.assertIsNotNone(response_data["articles"])
        self.assertEqual(len(response_data["articles"]), 1)
        self.assertEqual(response_data["count"], 1)

        article_data = response_data["articles"]
        self.assertIsNotNone(article_data)
        self.assertEqual(article_data[0]["title"], self.article_title)
        self.assertEqual(article_data[0]["description"], self.article_description)
        self.assertEqual(article_data[0]["tagList"], ["training"])
        self.assertEqual(article_data[0]["body"], self.article_body)
        self.assertEqual(article_data[0]["author"]["username"], "test_user")

    def test_get_article_with_slug(self):
        """
        test get article with slug
        """

        article: Article = Article.objects.create(
            title=self.article_title,
            author=self.user.profile,
            description=self.article_description,
            body=self.article_body,
        )

        tag = Tag.objects.create(tag="training")
        article.tags.set([tag])

        response = self.client.get(
            f"{self.article_url}/{article.slug}",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()
        self.assertIsNotNone(response_data)
        self.assertIsNotNone(response_data["article"])
        self.assertEqual(response_data["article"]["title"], self.article_title)
        self.assertEqual(
            response_data["article"]["description"], self.article_description
        )
        self.assertEqual(response_data["article"]["tagList"], ["training"])
        self.assertEqual(response_data["article"]["body"], self.article_body)
        self.assertEqual(response_data["article"]["author"]["username"], "test_user")

    def test_get_article_with_slug_not_found(self):
        """
        test get article with invalid slug
        """

        response = self.client.get(
            f"{self.article_url}/some_slug",
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.json(),
            self.not_found_response("Could not found any article with slug: some_slug"),
        )
