from flask import Flask , request , abort , jsonify
from flask_cors import CORS
from flask_sqlalchemy import sqlalchemy
from booksapp.models import setup_db , Book

books_per_page = 8 

def books_pagination(request , selection ):
    page = request.args.get('page' , 1 , int)
    start = (page-1)*books_per_page
    end = start + books_per_page
    books = [book.format() for book in selection]
    return books[start:end]


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    cors = CORS(app)
    
    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Headers","Content-Type,Authorization,True")
        response.headers.add("Access-Control-Allow-Methods" , "GET,POST,PATCH,DELETE,OPTIONS")
        return response
    
    @app.route('/books')
    def get_All_books():
        selection = Book.query.order_by(Book.id).all()
        current_books = books_pagination(request , selection)
        
        if len (current_books) == 0 :
            abort(404)

        return jsonify({
            "success":True , 
            "books":current_books , 
            "total_books":len(selection)
        })
    
    
    @app.route('/books/<int:book_id>' , methods=['PATCH'])
    def patch_book(book_id):
        body = request.get_json()
        try:  
            book = Book.query.filter(Book.id == book_id).one_or_none()
            if book is None:
                abort(404)
            if 'rating' in body:
                book.rating = int(body.get('rating')) 
            book.update()
            return jsonify({
                "success":True , 
                "book_id":book.id
            })
        except:
            abort(400)

    @app.route('/books/<int:book_id>' , methods=['DELETE'])
    def delete_book(book_id):
        try:
            book = Book.query.filter(Book.id == book_id).one_or_none()
            if book is None:
                abort(404)
            book.delete()
            
            selection = Book.query.order_by(Book.id).all()
            current_selection  = books_pagination(request , selection)
            
            return jsonify({
                "success":True , 
                "deleted_book":book.id , 
                "books":current_selection , 
                "total_books":len(selection)
            })
        except:
            abort(422)        
            
    
      

    
    @app.route('/books' , methods=['POST'])
    def post_book():
        
        body = request.get_json()
        title = body.get('title' , None)
        rating = int(body.get('rating' ,'1'))
        author = body.get('author')
        try:
            book = Book(title , author , rating)
            book.insert()
            selection = Book.query.order_by(Book.id).all()
            current_books = books_pagination(request , selection)
            return jsonify({
                "success":True , 
                "created":book.id , 
                "books":current_books,
                "total_books":len(selection)
            })
            return jsonify({"success":True})
        except:
            abort(422)
    
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success":False , 
            "error":404 , 
            "message":"Not Found"
        }) , 404
    
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success":False , 
            "error":422 , 
            "message":"Can not process your request"
            }) , 422
    
    return app
