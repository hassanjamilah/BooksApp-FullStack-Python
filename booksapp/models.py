import os
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
import json
db = SQLAlchemy()
database_path = 'postgres://postgres@localhost:5432/booksdb'
def setup_db(app , database_path):
   
    app.config['SQLALCHEMY_DATABASE_URI']=database_path
    app.config['SQLALCHEMY_HANDLE_MODIFICATIONS']=False
    db.app = app 
    db.init_app(app)
    db.create_all()


class Book(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    title = db.Column(db.String)
    author = db.Column(db.String)
    rating = db.Column(db.Integer)
    
    def __init__(self):
        self.title = None
        self.author = None
        self.rating = 1 
        
    def __init__(self,title , author , rating):
        self.title = title 
        self.author = author 
        self.rating = rating

    def format(self):
        return {
            "id":self.id , 
            "title":self.title , 
            "author":self.author , 
            "rating":self.rating
        }       
    
    def insert(self):
        db.session.add(self)
        db.session.commit()
        
    def update(self):
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()
