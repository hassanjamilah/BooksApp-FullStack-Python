from flask_sqlalchemy import SQLAlchemy
from booksapp import create_app
from booksapp.models import setup_db
import json
import unittest
from psycopg2 import _psycopg
class BooksTestCase (unittest.TestCase):
    def setUp(self):
       self.app = create_app()
       self.client = self.app.test_client
       self.database_path = 'postgres://postgres@localhost:5432/booksdb_test'
       setup_db(self.app , self.database_path)
       
       self.new_book = {
           "title":"book11" , 
           "author":"author1" , 
           "rating":"3"
       }
      
      
    
    def tearDown(self):
        pass
    
    
    def test_get_paginated_books(self):
        res = self.client.get('/books')
        data = json.load(res.data)
        
        self.assertEqual(res.status_code , 200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['total_books'])
        self.assertTrue(len(data['books']))
    
    def test_404_sent_request_beyond_valid_page(self):
        res = self.client.get('/books?page=1000' , json = {'rating':1})
        data = json.load(res.data)
        
        self.assertEqual(res.status_code , 200)
        self.assertEqual(data['success'] , False)
        self.assertEqual(data['message'] , 'Resource Not Found')  
    
    def test_get_books_search_with_result(self):
        res = self.client.post('/books' , json = {'search':'novel'})
        data = json.load(json.data)
        
        self.assertEqual(res.stats_code , 200)
        self.assertEqual(data['success' , True])
        self.assertTrue(data['total_books'])
        self.assertEqual(len(data['books']) , 4)
        
    def test_ge_books_search_without_results(self):
        res = self.client.post('/books' , json={'search':'kdjfksjl'})
        data = json.load(res.data)
        
        self.assertEqual(res.status_code , 200)
        self.assertEqual(data['success'] , True)
        self.assertEqual(data['total_books'] , 0)
        self.assertEqual(len(data['books'] , 0 ))
                         
                         
                         
    
    def test_given_behaviour(self):
        res = self.client.get('/')
        self.assertEqual(res.status_code ,200)
        
if __name__ == "__main__":
    unittest.main()