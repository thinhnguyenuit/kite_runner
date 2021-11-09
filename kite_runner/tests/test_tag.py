from .base import APIBaseTest


class TestTagAPI(APIBaseTest):

    def test_get_all_tags(self):
        """
        Test get all tags
        """
        response = self.client.get('/api/v1/tags/')
        self.assertEqual(response.status_code, 200)
