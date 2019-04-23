"""Application configuration file"""
import os


class Config:
    """Parent configuration class"""
    DEBUG = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    SECRET_KEY = os.getenv("SECRET_KEY")
    TESTING = False


class DevelopmentConfig(Config):
    """Development configuration class"""
    DEBUG = True


class TestingConfig(Config):
    """Testing configuration class"""
    DEBUG = True
    TESTING = True


class ProductionConfig(Config):
    """Production configuration class"""
    DEBUG = False


APP_CONFIG = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig
}
