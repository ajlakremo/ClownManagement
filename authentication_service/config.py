import os
from datetime import timedelta

from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS")
    JWT_SECRET_KEY = os.getenv("SECRET_KEY")
    JWT_TOKEN_LOCATION = ["headers", "cookies"]
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)


class DevelopmentConfig(Config):
    ENV = os.getenv("ENV")
    FLASK_DEBUG = os.getenv("FLASK_DEBUG")
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_ECHO = os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS")
    JWT_COOKIE_SECURE = os.getenv("JWT_COOKIE_SECURE")
