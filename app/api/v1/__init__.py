"""Entry point to the views"""
from flask import Blueprint
from flask_restful import Api

from app.api.v1.views.views import UserRegistration, UserLogin, UserInfo, \
    UserLogout

AUTH_BLUEPRINT = Blueprint("auth", __name__, url_prefix="/v1/auth")

AUTH = Api(AUTH_BLUEPRINT)

AUTH.add_resource(UserRegistration, "/signup")
AUTH.add_resource(UserLogin, "/login")
AUTH.add_resource(UserInfo, "/userinfo")
AUTH.add_resource(UserLogout, "/logout")
