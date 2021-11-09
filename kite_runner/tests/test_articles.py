from copy import deepcopy

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

    def setUp(self) -> None:
        super().setUp()
        self.article: Article = Article.objects.create(
            title=self.article_title,
            author=self.user.profile,
            description=self.article_description,
            body=self.article_body,
        )
        tags = []
        for tag_data in self.article_tag_list:
            tag = Tag.objects.create(tag=tag_data)
            tags.append(tag)
        self.article.tags.set(tags)

    def test_create_article(self) -> None:

        article_data = deepcopy(self.article_data)
        article_data["article"]["title"] = "How to train your dragon part 2"
        article_data["article"]["description"] = "Ever wonder how him got this far?"

        response = self.client.post(
            f"{self.article_url}",
            data=article_data,
            HTTP_AUTHORIZATION=TOKEN_HEADER.format(self.token[0].key),
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_data = response.json()
        self.assertIsNotNone(response_data)

        article_data = response_data["article"]
        self.assertIsNotNone(article_data)
        self.assertIsNotNone(article_data["slug"])
        self.assertEqual(article_data["title"], "How to train your dragon part 2")
        self.assertEqual(
            article_data["description"], "Ever wonder how him got this far?"
        )
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

    def test_create_article_with_invalid_token(self) -> None:
        response = self.client.post(
            f"{self.article_url}",
            data=self.article_data,
            HTTP_AUTHORIZATION=TOKEN_HEADER.format("invalid_token"),
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_article_without_token(self) -> None:
        response = self.client.post(f"{self.article_url}", data=self.article_data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json(), self.unauthenticated_response())

    def test_get_articles(self) -> None:  # sourcery skip: class-extract-method
        """
        test get recent articles globally
        """

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
        self.assertEqual(article_data[0]["tagList"], self.article_tag_list)
        self.assertEqual(article_data[0]["body"], self.article_body)
        self.assertEqual(article_data[0]["author"]["username"], "test_user")

    def test_get_article_by_slug(self) -> None:
        """
        test get article with slug
        """

        response = self.client.get(
            f"{self.article_url}/{self.article.slug}",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()
        self.assertIsNotNone(response_data)
        self.assertIsNotNone(response_data["article"])
        self.assertEqual(response_data["article"]["title"], self.article_title)
        self.assertEqual(
            response_data["article"]["description"], self.article_description
        )
        self.assertEqual(response_data["article"]["tagList"], self.article_tag_list)
        self.assertEqual(response_data["article"]["body"], self.article_body)
        self.assertEqual(response_data["article"]["author"]["username"], "test_user")

    def test_get_article_by_slug_not_found(self) -> None:
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

    def test_get_articles_by_author(self) -> None:

        response = self.client.get(
            f"{self.article_url}?author={self.user.username}",
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
        self.assertEqual(article_data[0]["tagList"], self.article_tag_list)
        self.assertEqual(article_data[0]["body"], self.article_body)
        self.assertEqual(article_data[0]["author"]["username"], "test_user")

    def test_get_articles_by_author_not_found(self) -> None:
        response = self.client.get(
            f"{self.article_url}?author=not_exist_author",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()["articles"]), 0)

    def test_get_articles_by_tag(self) -> None:
        response = self.client.get(
            f"{self.article_url}?tag=training",
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
        self.assertEqual(article_data[0]["tagList"], self.article_tag_list)
        self.assertEqual(article_data[0]["body"], self.article_body)
        self.assertEqual(article_data[0]["author"]["username"], "test_user")

    def test_get_articles_by_tag_not_found(self) -> None:
        response = self.client.get(f"{self.article_url}?tag=not_found_tag")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()["articles"]), 0)

    def test_update_article(self) -> None:

        updated_article_data = {
            "article": {
                "title": "updated_title",
                "description": "updated_description",
                "body": "updated_body",
                "tagList": ["updated_tag1", "updated_tag2"],
            }
        }
        response = self.client.put(
            f"{self.article_url}/{self.article.slug}",
            data=updated_article_data,
            HTTP_AUTHORIZATION=TOKEN_HEADER.format(self.token[0].key),
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["article"]["title"], "updated_title")
        self.assertEqual(
            response.json()["article"]["description"], "updated_description"
        )
        self.assertEqual(response.json()["article"]["body"], "updated_body")
        self.assertEqual(
            response.json()["article"]["tagList"], ["updated_tag1", "updated_tag2"]
        )

    def test_favorite_article(self) -> None:

        response = self.client.post(
            f"{self.article_url}/{self.article.slug}/favorite/",
            HTTP_AUTHORIZATION=TOKEN_HEADER.format(self.token[0].key),
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response_data = response.json()
        self.assertIsNotNone(response_data)
        self.assertIsNotNone(response_data["article"])
        self.assertEqual(response_data["article"]["title"], self.article_title)
        self.assertEqual(
            response_data["article"]["description"], self.article_description
        )
        self.assertEqual(response_data["article"]["tagList"], self.article_tag_list)
        self.assertEqual(response_data["article"]["body"], self.article_body)
        self.assertEqual(response_data["article"]["favoritesCount"], 1)
        self.assertEqual(response_data["article"]["favorited"], True)

    def test_favorite_article_already_favorited(self) -> None:

        response = self.client.post(
            f"{self.article_url}/{self.article.slug}/favorite/",
            HTTP_AUTHORIZATION=TOKEN_HEADER.format(self.token[0].key),
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_favorite_article_not_found(self) -> None:

        response = self.client.post(
            f"{self.article_url}/not_exist_slug/favorite/",
            HTTP_AUTHORIZATION=TOKEN_HEADER.format(self.token[0].key),
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.json(),
            self.not_found_response(
                "Could not found any article with slug: not_exist_slug"
            ),
        )

    def test_get_article_feed(self) -> None:

        response = self.client.get(
            f"{self.article_url}/feed/",
            HTTP_AUTHORIZATION=TOKEN_HEADER.format(self.token[0].key),
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()["articles"]), 1)

    def test_get_article_feed_not_found(self) -> None:

        response = self.client.get(
            f"{self.article_url}/feed/",
            HTTP_AUTHORIZATION=TOKEN_HEADER.format(self.token[0].key),
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()["articles"]), 0)
