"""Module for the user view"""
from flask import abort
from flask_restful import Resource, reqparse

from app.api.v1.models.models import UserModel


class UserRegistration(Resource):
    """
    User Registration Resource
    """
    def post(self):
        """Create a user account"""
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument(
            "firstname",
            type=str, required=True, help="firstname cannot be blank")
        parser.add_argument(
            "lastname",
            type=str, required=True, help="lastname cannot be blank")
        parser.add_argument(
            "email",
            type=str, required=True, help="email cannot be blank")
        parser.add_argument(
            "password",
            type=str, required=True, help="password cannot be blank")

        data = parser.parse_args()

        # Create an instance of a user
        user = UserModel(
            firstname=data["firstname"],
            lastname=data["lastname"],
            email=data["email"],
            password=data["password"]
        )

        if user.find_user_by_email(data["email"]):
            abort(409, {
                "error": "Email address '{}' is taken!".format(data["email"]),
                "status": 409
            })

        user.save()

        result = user.find_user_by_email(data["email"])
        auth_token = user.encode_auth_token(result["id"])

        return {
            "status": 201,
            "user": UserModel.to_json(result),
            "auth_token": auth_token.decode(),
            "message": "User account was created successfully"
        }, 201


class UserLogin(Resource):
    """
    User Login Resource
    """
    def post(self):
        """Login to a user account"""
        user = UserModel()

        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument(
            "email",
            type=str, required=True, help="email cannot be blank"
        )
        parser.add_argument(
            "password",
            type=str, required=True, help="password cannot be blank")

        data = parser.parse_args()

        current_user = user.find_user_by_email(data["email"])

        if not current_user:
            abort(404, {
                "error": "Wrong email address or password!",
                "status": 404
            })

        auth_token = user.encode_auth_token(current_user["id"])
        return {
            "status": 201,
            "user": user.to_json(current_user),
            "auth_token": auth_token.decode(),
            "message": "You have successfully logged in"
        }, 200
