# Bookstore Management System API

This project provides a RESTful API for managing a bookstore, allowing users to perform operations such as adding, retrieving, updating, and deleting book information.

## Features

- **Database Schema**: Utilizes a MySQL database to store book details, including title, author, ISBN, price, and quantity.
- **API Endpoints**: Provides endpoints for performing CRUD operations on books:
  - Adding a new book
  - Retrieving all books
  - Retrieving a specific book by ISBN
  - Updating book details
  - Deleting a book
- **Authentication**: Implements basic authentication to restrict access to certain endpoints.
- **Documentation**: Includes Swagger/OpenAPI Specification for clear documentation of API endpoints and usage.
- **Testing**: Provides unit tests for the API endpoints to ensure functionality and handle edge cases and errors effectively.

## Technologies Used

- Flask: Python web framework for developing the RESTful API.
- Flask-SQLAlchemy: SQLAlchemy integration for database management.
- Flask-HTTPAuth: Library for implementing basic authentication in Flask applications.
- Flask-Swagger: Integration of Swagger/OpenAPI Specification for API documentation.
- MySQL: Relational database management system for storing book details.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your_username/bookstore-api.git
```
