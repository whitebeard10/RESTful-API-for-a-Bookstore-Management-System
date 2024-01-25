from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from flasgger import Swagger
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/books'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.urandom(24)  # Secret key for authentication
db = SQLAlchemy(app)
auth = HTTPBasicAuth()
swagger = Swagger(app, template_file='../docs/bookstore_api.yaml')  

# Database model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    isbn = db.Column(db.String(13), unique=True, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

users = {
    "admin": "password"
}

# Basic authentication
@auth.verify_password
def verify_password(username, password):
    """Verify the username and password."""
    if username in users and users[username] == password:
        return username

# Unauthorized access response
@auth.error_handler
def unauthorized():
    """Unauthorized access response."""
    return jsonify({'message': 'Unauthorized access'}), 401

# API endpoints 
@app.route('/books', methods=['POST'])
@auth.login_required
def add_book():
    """Add a new book to the bookstore."""
    data = request.get_json()
    new_book = Book(title=data['title'], author=data['author'], isbn=data['isbn'],
                    price=data['price'], quantity=data['quantity'])
    db.session.add(new_book)
    db.session.commit()
    return jsonify({'message': 'Book added successfully'}), 201

@app.route('/books', methods=['GET'])
def get_all_books():
    """Retrieve all books from the bookstore."""
    books = Book.query.all()
    output = [{'title': book.title, 'author': book.author, 'isbn': book.isbn,
               'price': float(book.price), 'quantity': book.quantity} for book in books]
    return jsonify({'books': output})

@app.route('/books/<isbn>', methods=['GET'])
def get_book(isbn):
    """Retrieve a specific book by ISBN."""
    book = Book.query.filter_by(isbn=isbn).first()
    if not book:
        return jsonify({'message': 'Book not found'}), 404
    book_data = {'title': book.title, 'author': book.author, 'isbn': book.isbn,
                 'price': float(book.price), 'quantity': book.quantity}
    return jsonify({'book': book_data})

@app.route('/books/<isbn>', methods=['PUT'])
@auth.login_required
def update_book(isbn):
    """Update details of a specific book by ISBN."""
    book = Book.query.filter_by(isbn=isbn).first()
    if not book:
        return jsonify({'message': 'Book not found'}), 404
    data = request.get_json()
    book.title = data['title']
    book.author = data['author']
    book.price = data['price']
    book.quantity = data['quantity']
    db.session.commit()
    return jsonify({'message': 'Book updated successfully'})

@app.route('/books/<isbn>', methods=['DELETE'])
@auth.login_required
def delete_book(isbn):
    """Delete a specific book by ISBN."""
    book = Book.query.filter_by(isbn=isbn).first()
    if not book:
        return jsonify({'message': 'Book not found'}), 404
    db.session.delete(book)
    db.session.commit()
    return jsonify({'message': 'Book deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)
