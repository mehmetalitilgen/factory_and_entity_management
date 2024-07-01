# REST API Development Case

This project is a REST API developed using Python Flask and MongoDB. It includes user authentication and factory/entity
management with pagination support.

## Requirements

- Backend Framework: Flask
- Database: MongoDB
- Authentication: JWT (JSON Web Token)

## Installation

1. Clone the repository:
    ```
    git clone <repository-url>
    cd <repository-directory>
    ```

2. Create a virtual environment and activate it:
    ```
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the dependencies:
    ```
    pip install -r requirements.txt
    ```

4. Set up environment variables in a `.env` file:
    ```
    MONGO_URI=<mongo-uri>
    JWT_SECRET_KEY=<jwt-secret-key>
    ```

5. Run the application:
    ```
    flask run
    ```

## Endpoints

### User Endpoints

- `POST /register`: Register a new user
- `POST /login`: Login a user
- `POST /refresh`: Refresh JWT token
- `POST /logout`: Logout a user
- `GET /user/<user_id>`: Get user details
- `DELETE /user/<user_id>`: Delete a user

### Factory Endpoints

- `POST /factory`: Add a new factory
- `GET /factory/<factory_id>`: Get factory details
- `PUT /factory/<factory_id>`: Update factory details
- `DELETE /factory/<factory_id>`: Delete a factory

### Entity Endpoints

- `POST /entity`: Add a new entity
- `GET /entity/<entity_id>`: Get entity details
- `PUT /entity/<entity_id>`: Update entity details
- `DELETE /entity/<entity_id>`: Delete an entity

## Running Tests

1. Ensure the virtual environment is activated:
    ```
   source .venv/bin/activate
    ```

2. Run the tests:
    ```
    python -m unittest  tests/user_test.py
    python -m unittest  tests/factory_test.py
    python -m unittest  tests/entity_test.py 

    ```
