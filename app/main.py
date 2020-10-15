import os

from flask import Flask
from flask_restx import Api, Resource, reqparse, inputs
from flask_sqlalchemy import SQLAlchemy

config_file = os.environ.get("CONFIG", "app.config")

app = Flask(__name__)
app.config.from_object(config_file)
db = SQLAlchemy(app)
api = Api(app)
