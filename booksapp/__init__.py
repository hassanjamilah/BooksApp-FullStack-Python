from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import sqlalchemy
from booksapp.models import setup_db , Book

def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    cors = CORS(app)
    return app
