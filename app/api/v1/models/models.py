"""Use entity module"""
import os
from os.path import join, dirname
from datetime import datetime, timedelta

import jwt
from dotenv import load_dotenv

from app.api.v1.models.base_model import BaseModel
from app.api.v1.models.queries import insert_user_query

DOTENV_PATH = join(dirname(__file__), ".env")

load_dotenv(DOTENV_PATH)


class UserModel(BaseModel):
    """Entity representation for a user"""
    def __init__(self, **kwargs):
        super().__init__()
        self.firstname = kwargs.get("firstname")
        self.lastname = kwargs.get("lastname")
        self.email = kwargs.get("email")
        self.password = kwargs.get("password")
        self.registered = str(datetime.utcnow())

    def save(self):
        """Add a new user to the 'users' table"""
        query = insert_user_query().format(
            self.firstname,
            self.lastname,
            self.email,
            self.password
        )
        self.cursor.execute(query)
        self.connection.commit()

    def find_user_by_email(self, value):
        """Find a user by his/her email address"""
        result = self.search_user("email", value)
        return result

    def encode_auth_token(self, user_id):
        """Encode the authentication token"""
        try:
            payload = {
                "sub": user_id,
                "iat": datetime.utcnow(),
                "exp": datetime.utcnow() + timedelta(seconds=30)
            }
            return jwt.encode(
                payload,
                os.getenv("JWT_SECRET_KEY"),
                algorithm="HS256"
            )
        except Exception as jwt_exception:
            return jwt_exception

    @staticmethod
    def decode_auth_token(auth_token):
        """Decode the authentication token"""
        try:
            payload = jwt.decode(
                auth_token,
                os.getenv("JWT_SECRET_KEY"),
                algorithms="HS256"
            )
            return payload["sub"]
        except jwt.ExpiredSignatureError:
            return "Signature expired. Please log in again."
        except jwt.InvalidTokenError:
            return "Invalid token. Please log in again."

    @staticmethod
    def to_json(result):
        """Return a JSON representation of the user's info"""
        return {
            "id": result["id"],
            "firstname": result["firstname"],
            "lastname": result["lastname"],
            "email": result["email"],
            "isAdmin": result["is_admin"],
            "registered": str(result["registered_on"]),
        }
