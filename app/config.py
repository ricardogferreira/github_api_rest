import os

GITHUB_API_URL = "https://api.github.com"

# Flask-Sqlalchemy settings
SQLALCHEMY_TRACK_MODIFICATIONS = False
POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
POSTGRES_ADDRESS = os.environ.get("POSTGRES_ADDRESS", 'localhost')

if POSTGRES_USER and POSTGRES_PASSWORD and POSTGRES_ADDRESS:
    SQLALCHEMY_DATABASE_URI = "postgresql://{}:{}@{}:5432/github_api".format(
        POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_ADDRESS
    )
else:
    SQLALCHEMY_DATABASE_URI = "sqlite:////tmp/test.db"

SECRET_KEY = os.environ.get("SECRET_KEY", "123444")
