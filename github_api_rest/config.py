import os

GITHUB_API_URL = "https://api.github.com"

# Flask-Sqlalchemy settings
SQLALCHEMY_TRACK_MODIFICATIONS = False
POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
POSTGRES_ADDRESS = os.environ.get("POSTGRES_ADDRESS", "localhost")
POSTGRES_DB = os.environ.get("POSTGRES_DB", "github_api")

if all([POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_ADDRESS, POSTGRES_DB]):
    SQLALCHEMY_DATABASE_URI = "postgresql://{}:{}@{}:5432/{}".format(
        POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_ADDRESS, POSTGRES_DB
    )
else:
    SQLALCHEMY_DATABASE_URI = "sqlite:////tmp/test.db"

SECRET_KEY = os.environ.get("SECRET_KEY", "123444")
