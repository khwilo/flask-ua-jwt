"""Module for the user view"""
from flask import abort, request
from flask_restful import Resource, reqparse

from app.api.v1.models.models import UserModel, BlackListTokenModel


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
            "status": 200,
            "auth_token": auth_token.decode(),
            "message": "You have successfully logged in"
        }, 200


class UserInfo(Resource):
    """
    User information resource
    """
    def get(self):
        """Fetch a user's information"""
        auth_header = request.headers.get("Authorization")
        if auth_header:
            try:
                auth_token = auth_header.split(" ")[1]
            except IndexError:
                abort(401, {
                    "error": "Bearer token is malformed"
                })
        else:
            auth_token = " "
        if auth_token:
            response = UserModel.decode_auth_token(auth_token)
            if not isinstance(response, str):
                user = UserModel().search_user("id", response)
                return {
                    "status": 200,
                    "user": UserModel.to_json(user)
                }, 200
            abort(401, {
                "status": 401,
                "error": response
            })
        else:
            abort(401, {
                "status": 401,
                "error": "Please provide a valid authentication token"
            })


class UserLogout(Resource):
    """
    User Logout Resource
    """
    def post(self):
        """Logout a user"""
        auth_header = request.headers.get("Authorization")
        if auth_header:
            try:
                auth_token = auth_header.split(" ")[1]
            except IndexError:
                abort(401, {
                    "error": "Bearer token is malformed"
                })
        else:
            auth_token = " "
        if auth_token:
            response = UserModel.decode_auth_token(auth_token)
            if not isinstance(response, str):
                blacklist_token = BlackListTokenModel(token=auth_token)
                try:
                    blacklist_token.save()
                    return {
                        "status": 200,
                        "message": "You have successfully logged out"
                    }
                except Exception as exception:
                    abort(401, {
                        "status": 401,
                        "error": exception
                    })
            else:
                abort(401, {
                    "status": 401,
                    "error": response
                })
        else:
            abort(403, {
                "status": 403,
                "error": "Please provide a valid authentication token"
            })
