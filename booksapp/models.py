import os
from flask_sqlalchemy import SQLAlchemy
import json
db = SQLAlchemy()
database_uri = 'postgres://postgres@localhost:5432/booksdb'
def setup_db(app):
   
    app.config['SQLALCHEMY_DATABASE_URI']=database_uri
    app.config['SQLALCHEMY_HANDLE_MODIFICATIONS']=False
    db.app = app 
    db.init_app(app)
    db.create_all()


class Book(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    title = db.Column(db.String)
    author = db.Column(db.String)
    rating = db.Column(db.Integer)
    
