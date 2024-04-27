# Project Documentation

## Overview
This project is a Django-based application that provides a set of APIs for user management, prize management, and password reset functionalities. Below is the documentation for the available APIs and how to interact with them.

## API Endpoints

### User Management

#### Create User
- **Endpoint:** `/api/user/create/`
- **Method:** POST
- **Description:** Allows the creation of a new user.
- **Payload:**
  ```json
  {
    "email": "user@example.com",
    "password": "securepassword",
    "name": "John Doe",
    "phone": "1234567890"
  }
  ```

#### Obtain Auth Token
- **Endpoint:** `/api/user/token/`
- **Method:** POST
- **Description:** Obtain an authentication token for a user.
- **Payload:**
  ```json
  {
    "email": "user@example.com",
    "password": "securepassword"
  }
  ```

#### Manage User
- **Endpoint:** `/api/user/me/`
- **Method:** GET, PUT
- **Description:** Retrieve or update the authenticated user's information.
- **Headers:** `Authorization: Token <your_token>`

### Prize Management

#### List Prizes
- **Endpoint:** `/api/prize/`
- **Method:** GET
- **Description:** Lists all available prizes.
- **Headers:** `Authorization: Token <your_token>`

#### Create Prize
- **Endpoint:** `/api/prize/create/`
- **Method:** POST
- **Description:** Create a new prize (Admin only).
- **Payload:**
  ```json
  {
    "name": "New Prize",
    "remaining_quantity": 100
  }
  ```
- **Headers:** `Authorization: Token <your_token>`

### Password Reset

#### Request Password Reset
- **Endpoint:** `/api/user/reset_password/`
- **Method:** POST
- **Description:** Request a password reset link.
- **Payload:**
  ```json
  {
    "email": "user@example.com",
    "url": "http://example.com/reset_password"
  }
  ```

#### Reset Password
- **Endpoint:** `/api/user/reset_password/<uuid>/`
- **Method:** PUT
- **Description:** Reset the user's password using the link received.
- **Payload:**
  ```json
  {
    "password": "newsecurepassword"
  }
  ```

## Setup and Installation

1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up the database:
   ```bash
   python manage.py migrate
   ```
4. Run the server:
   ```bash
   python manage.py runserver
   ```

## Testing

To test the APIs, you can use tools like Postman or cURL. Ensure you have the correct authorization headers when required.

This documentation provides a basic overview of the APIs. For more detailed information, refer to the codebase and comments within the code.