from flask import Flask, jsonify
from _utilities import get_available_books

# instantiate Flask
app=Flask(__name__)

@app.route('/books')
def get_books():
    return jsonify({'books':get_available_books()})


@app.route('/books/<int:isbn>')
def get_book_by_isbn(isbn):
    intended_book = {}
    available_books = get_available_books()
    for book in available_books:
        if book['isbn'] == str(isbn):
            intended_book = book
    return jsonify(intended_book)
            
app.run(port=5000)
