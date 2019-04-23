"""Module for the user view"""
from flask_restful import Resource


class UserRegistration(Resource):
    """
    User Registration Resource
    """

    def get(self):
        """
        Welcome message
        """
        return {
            "status": 200,
            "message": "Welcome to Flask UA"
        }, 200
