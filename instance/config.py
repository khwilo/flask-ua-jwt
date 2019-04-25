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
    DATABASE_URL = os.getenv("DATABASE_URL")


class TestingConfig(Config):
    """Testing configuration class"""
    DEBUG = True
    TESTING = True
    DATABASE_URL = os.getenv("DATABASE_TEST_URL")


class StagingConfig(Config):
    """Staging configuration class"""
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration class"""
    DEBUG = False


APP_CONFIG = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig
}
