"""Entry point for the API"""
from flask import Flask

from app.api.v1 import AUTH_BLUEPRINT


def create_app():
    """
    Instantiate the Flask API
    """
    app = Flask(__name__)

    app.register_blueprint(AUTH_BLUEPRINT)

    return app
