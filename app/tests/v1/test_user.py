"""Test cases for the user authentication"""
import json

from app.tests.v1.test_base import BaseTestCase


class UserTestCase(BaseTestCase):
    """Test definitions for user authentication"""
    def test_user_registration(self):
        """Test a user can register for an account"""
        res = self.client.get(
            "/v1/auth/signup",
            headers=BaseTestCase.get_accept_content_type_headers()
        )
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(res.status_code, 200)
        self.assertTrue(response_msg["message"])
        self.assertEqual(response_msg["message"], "Welcome to Flask UA")
