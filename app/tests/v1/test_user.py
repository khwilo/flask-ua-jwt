"""Test cases for the user authentication"""
import json
import time

from app.api.v1.models.models import UserModel
from app.tests.v1.sample_data import USER_REGISTRATION, USER_LOGIN, \
    USER_NOT_FOUND
from app.tests.v1.test_base import BaseTestCase


class UserTestCase(BaseTestCase):
    """Test definitions for user authentication"""
    def test_user_registration(self):
        """Test a user can register for an account"""
        res = self.client.post(
            "/v1/auth/signup",
            headers=BaseTestCase.get_accept_content_type_headers(),
            data=json.dumps(USER_REGISTRATION)
        )
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(res.status_code, 201)
        self.assertTrue(response_msg["message"])
        self.assertTrue(response_msg["auth_token"])
        self.assertEqual(
            response_msg["message"],
            "User account was created successfully"
        )

    def test_duplicate_email(self):
        """Test that the email address is unique for all accounts"""
        res = self.client.post(
            "/v1/auth/signup",
            headers=BaseTestCase.get_accept_content_type_headers(),
            data=json.dumps(USER_REGISTRATION)
        )
        res = self.client.post(
            "/v1/auth/signup",
            headers=BaseTestCase.get_accept_content_type_headers(),
            data=json.dumps(USER_REGISTRATION)
        )
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(res.status_code, 409)
        self.assertEqual(
            response_msg["message"]["error"],
            "Email address 'foo123@example.com' is taken!"
        )

    def test_encode_auth_token(self):
        """Test that the authentication token is created"""
        user = UserModel(
            firstname="Jane",
            lastname="Doe",
            email="jane@example.com",
            password="doe123jo"
        )
        user.save()
        user_id = user.find_user_by_email("jane@example.com")["id"]
        auth_token = user.encode_auth_token(user_id)
        self.assertTrue(isinstance(auth_token, bytes))

    def test_decode_auth_token(self):
        """Test that the authentication token can be decoded"""
        user = UserModel(
            firstname="Jane",
            lastname="Doe",
            email="jane@example.com",
            password="doe123jo"
        )
        user.save()
        user_id = user.find_user_by_email("jane@example.com")["id"]
        auth_token = user.encode_auth_token(user_id)
        self.assertTrue(isinstance(auth_token, bytes))
        self.assertEqual(UserModel.decode_auth_token(auth_token), 1)

    def test_user_login(self):
        """Test that a user can be able to login"""
        res = self.client.post(
            "/v1/auth/signup",
            headers=BaseTestCase.get_accept_content_type_headers(),
            data=json.dumps(USER_REGISTRATION)
        )
        self.assertEqual(res.status_code, 201)
        res = self.client.post(
            "/v1/auth/login",
            headers=BaseTestCase.get_accept_content_type_headers(),
            data=json.dumps(USER_LOGIN)
        )
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(res.status_code, 200)
        self.assertTrue(response_msg["auth_token"])
        self.assertTrue(response_msg["message"])
        self.assertEqual(
            response_msg["message"],
            "You have successfully logged in"
        )

    def test_user_not_found(self):
        """Test that an unregistered user cannot log in"""
        res = self.client.post(
            "/v1/auth/login",
            headers=BaseTestCase.get_accept_content_type_headers(),
            data=json.dumps(USER_NOT_FOUND)
        )
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(res.status_code, 404)
        self.assertEqual(
            response_msg["message"]["error"],
            "Wrong email address or password!"
        )

    def test_fetch_user_info(self):
        """Test the API can fetch the user's information"""
        res = self.client.post(
            "/v1/auth/signup",
            headers=BaseTestCase.get_accept_content_type_headers(),
            data=json.dumps(USER_REGISTRATION)
        )
        self.assertEqual(res.status_code, 201)
        res = self.client.post(
            "/v1/auth/login",
            headers=BaseTestCase.get_accept_content_type_headers(),
            data=json.dumps(USER_LOGIN)
        )
        self.assertEqual(res.status_code, 200)
        auth_token = json.loads(res.data.decode("UTF-8"))["auth_token"]
        res = self.client.get(
            "/v1/auth/userinfo",
            headers=BaseTestCase.get_authentication_headers(auth_token),
        )
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(response_msg["user"]["firstname"], "foo")
        self.assertEqual(response_msg["user"]["lastname"], "bar")
        self.assertEqual(response_msg["user"]["email"], "foo123@example.com")

    def test_user_logout(self):
        """Test that a user can logout"""
        res = self.client.post(
            "/v1/auth/signup",
            headers=BaseTestCase.get_accept_content_type_headers(),
            data=json.dumps(USER_REGISTRATION)
        )
        self.assertEqual(res.status_code, 201)
        res = self.client.post(
            "/v1/auth/login",
            headers=BaseTestCase.get_accept_content_type_headers(),
            data=json.dumps(USER_LOGIN)
        )
        self.assertEqual(res.status_code, 200)
        auth_token = json.loads(res.data.decode("UTF-8"))["auth_token"]
        res = self.client.post(
            "/v1/auth/logout",
            headers=BaseTestCase.get_authentication_headers(auth_token)
        )
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(res.status_code, 200)
        self.assertTrue(response_msg["message"])
        self.assertTrue(response_msg["status"])
        self.assertEqual(
            response_msg["message"],
            "You have successfully logged out"
        )
        self.assertEqual(response_msg["status"], 200)

    def test_user_logout_missing_token(self):
        """Test missing authentication token on user logout"""
        res = self.client.post(
            "/v1/auth/signup",
            headers=BaseTestCase.get_accept_content_type_headers(),
            data=json.dumps(USER_REGISTRATION)
        )
        self.assertEqual(res.status_code, 201)
        res = self.client.post(
            "/v1/auth/login",
            headers=BaseTestCase.get_accept_content_type_headers(),
            data=json.dumps(USER_LOGIN)
        )
        self.assertEqual(res.status_code, 200)
        auth_token = ""
        res = self.client.post(
            "/v1/auth/logout",
            headers=BaseTestCase.get_authentication_headers(auth_token)
        )
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(res.status_code, 403)
        self.assertTrue(response_msg["message"]["error"])
        self.assertTrue(response_msg["message"]["status"])
        self.assertEqual(
            response_msg["message"]["error"],
            "Please provide a valid authentication token"
        )
        self.assertEqual(response_msg["message"]["status"], 403)

    def test_user_log_out_expired_token(self):
        """Test expired authentication token on user logout"""
        res = self.client.post(
            "/v1/auth/signup",
            headers=BaseTestCase.get_accept_content_type_headers(),
            data=json.dumps(USER_REGISTRATION)
        )
        self.assertEqual(res.status_code, 201)
        res = self.client.post(
            "/v1/auth/login",
            headers=BaseTestCase.get_accept_content_type_headers(),
            data=json.dumps(USER_LOGIN)
        )
        self.assertEqual(res.status_code, 200)
        auth_token = json.loads(res.data.decode("UTF-8"))["auth_token"]
        time.sleep(31)
        res = self.client.post(
            "/v1/auth/logout",
            headers=BaseTestCase.get_authentication_headers(auth_token)
        )
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(res.status_code, 401)
        self.assertTrue(response_msg["message"]["error"])
        self.assertTrue(response_msg["message"]["status"])
        self.assertEqual(
            response_msg["message"]["error"],
            "Signature expired. Please log in again."
        )
        self.assertEqual(response_msg["message"]["status"], 401)
