"""Entry point to the views"""
from flask import Blueprint
from flask_restful import Api

from app.api.v1.views.views import UserRegistration

AUTH_BLUEPRINT = Blueprint("auth", __name__, url_prefix="/v1/auth")

AUTH = Api(AUTH_BLUEPRINT)

AUTH.add_resource(UserRegistration, "/signup")
