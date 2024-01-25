import unittest
import json
import base64
from app import app, db, Book

class TestApp(unittest.TestCase):
    def setUp(self):
        """Set up test environment before each test."""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/test_books'  # Temporary MySQL testing database
        self.app = app.test_client()

        # Create application context
        self.app_context = app.app_context()
        self.app_context.push()

        # Create all tables in the database
        db.create_all()

    def tearDown(self):
        """Clean up test environment after each test."""
        db.session.remove()

        # Drop all tables and remove application context
        db.drop_all()
        self.app_context.pop()

    def get_auth_header(self, username, password):
        """Get the Authorization header with basic authentication."""
        credentials = f"{username}:{password}"
        encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
        return {'Authorization': 'Basic ' + encoded_credentials}

    def test_add_book(self):
        """Test adding a new book."""
        # Valid request with correct data and authentication
        response = self.app.post('/books', json={
            'title': 'Test Book',
            'author': 'Test Author',
            'isbn': '1234567890123',
            'price': 19.99,
            'quantity': 10
        }, headers=self.get_auth_header('admin', 'password'))
        self.assertEqual(response.status_code, 201)


    def test_get_all_books(self):
        """Test retrieving all books."""
        # Add a book to the database
        book = Book(title='Test Book', author='Test Author', isbn='1234567890123', price=19.99, quantity=10)
        db.session.add(book)
        db.session.commit()

        # Retrieve all books
        response = self.app.get('/books')
        data = json.loads(response.data)
        self.assertEqual(len(data['books']), 1)
        self.assertEqual(response.status_code, 200)

    def test_get_book(self):
        """Test retrieving a specific book by ISBN."""
        # Add a book to the database
        book = Book(title='Test Book', author='Test Author', isbn='1234567890123', price=19.99, quantity=10)
        db.session.add(book)
        db.session.commit()

        # Retrieve the added book by its ISBN
        response = self.app.get('/books/1234567890123')
        data = json.loads(response.data)
        self.assertEqual(data['book']['title'], 'Test Book')
        self.assertEqual(response.status_code, 200)

        # Try to retrieve a non-existent book
        response = self.app.get('/books/1234567890124')
        self.assertEqual(response.status_code, 404)

    def test_update_book(self):
        """Test updating book details."""
        # Add a book to the database
        book = Book(title='Test Book', author='Test Author', isbn='1234567890123', price=19.99, quantity=10)
        db.session.add(book)
        db.session.commit()

        # Update the added book
        response = self.app.put('/books/1234567890123', json={
            'title': 'Updated Book',
            'author': 'Updated Author',
            'price': 29.99,
            'quantity': 5
        }, headers=self.get_auth_header('admin', 'password'))
        self.assertEqual(response.status_code, 200)

        # Retrieve the updated book and check if details are updated
        response = self.app.get('/books/1234567890123')
        data = json.loads(response.data)
        self.assertEqual(data['book']['title'], 'Updated Book')
        self.assertEqual(data['book']['author'], 'Updated Author')
        self.assertEqual(data['book']['price'], 29.99)
        self.assertEqual(data['book']['quantity'], 5)

    def test_delete_book(self):
        """Test deleting a book."""
        # Add a book to the database
        book = Book(title='Test Book', author='Test Author', isbn='1234567890123', price=19.99, quantity=10)
        db.session.add(book)
        db.session.commit()

        # Delete the added book
        response = self.app.delete('/books/1234567890123', headers=self.get_auth_header('admin', 'password'))
        self.assertEqual(response.status_code, 200)

        # Try to retrieve the deleted book
        response = self.app.get('/books/1234567890123')
        self.assertEqual(response.status_code, 404)

    def test_unauthorized_access(self):
        """Test unauthorized access to protected endpoints."""
        # Attempt to add a book without authentication
        response = self.app.post('/books', json={
            'title': 'Unauthorized Book',
            'author': 'Unauthorized Author',
            'isbn': '1234567890124',
            'price': 29.99,
            'quantity': 5
        })
        self.assertEqual(response.status_code, 401)

        # Attempt to update a book without authentication
        response = self.app.put('/books/1234567890123', json={
            'title': 'Updated Unauthorized Book',
            'author': 'Updated Unauthorized Author',
            'price': 29.99,
            'quantity': 5
        })
        self.assertEqual(response.status_code, 401)

        # Attempt to delete a book without authentication
        response = self.app.delete('/books/1234567890123')
        self.assertEqual(response.status_code, 401)

if __name__ == '__main__':
    unittest.main()
