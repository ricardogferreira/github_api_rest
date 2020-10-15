import os

from flask import Flask
from flask_restx import Api, Resource, reqparse, inputs
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

config_file = os.environ.get("CONFIG", "app.config")

app = Flask(__name__)
app.config.from_object(config_file)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app)
