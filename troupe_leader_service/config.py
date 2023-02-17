import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS")


class DevelopmentConfig(Config):
    ENV = os.getenv("ENV")
    FLASK_DEBUG = os.getenv("FLASK_DEBUG")
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_ECHO = os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS")
