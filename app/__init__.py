"""Entry point for the API"""
from flask import Flask

from app.api.v1 import AUTH_BLUEPRINT

from instance.config import APP_CONFIG


def create_app(config_name):
    """
    Instantiate the Flask API
    """
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(APP_CONFIG[config_name])
    app.config.from_pyfile("config.py")

    app.register_blueprint(AUTH_BLUEPRINT)

    return app
