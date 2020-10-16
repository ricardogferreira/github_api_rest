import os

from flask import Flask
from flask_migrate import Migrate
from flask_restx import Api, Resource, inputs, reqparse
from flask_sqlalchemy import SQLAlchemy

config_file = os.environ.get("CONFIG", "github_api_rest.config")

app = Flask(__name__)
app.config.from_object(config_file)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app)
