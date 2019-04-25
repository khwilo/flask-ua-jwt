"""Base test definitions"""
import os
import unittest

from app import create_app
from manage import establish_connection, migrate_test, destroy


class BaseTestCase(unittest.TestCase):
    """Base class for other test cases"""
    def setUp(self):
        self.app = create_app(config_name="testing")
        self.app_context = self.app.app_context()
        self.client = self.app.test_client()
        self.app_context.push()

        with self.app_context:
            self.connection = establish_connection()
            self.database_url = os.getenv("DATABASE_TEST_URL")
            migrate_test()

    def tearDown(self):
        destroy(self.database_url)
        self.connection.close()
        self.app_context.pop()

    @staticmethod
    def get_accept_content_type_headers():
        """Return the content type headers"""
        content_type = {}
        content_type["Accept"] = "application/json"
        content_type["Content-Type"] = "application/json"
        return content_type

if __name__ == "__main__":
    unittest.main()
