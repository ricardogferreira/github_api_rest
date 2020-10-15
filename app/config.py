import os

GITHUB_API_URL = "https://api.github.com"

# Flask-Sqlalchemy settings
SQLALCHEMY_TRACK_MODIFICATIONS = False
POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")

if POSTGRES_USER and POSTGRES_PASSWORD:
    SQLALCHEMY_DATABASE_URI = "postgresql://{}:{}@postgres:5432/github_api".format(
        POSTGRES_USER, POSTGRES_PASSWORD
    )
else:
    SQLALCHEMY_DATABASE_URI = "sqlite:////tmp/test.db"

SECRET_KEY = os.environ.get("SECRET_KEY", "123444")
