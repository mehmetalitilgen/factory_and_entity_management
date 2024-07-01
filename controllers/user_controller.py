from models.user_model import create_user, find_user_by_id, find_user_by_username, delete_user_by_id
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token


def user_register_controller(data):
    if data["password"] != data["confirm_password"]:
        return {"status": "error", "message": "Passwords do not match."}, 400

    existing_user = find_user_by_username(data["username"])
    if existing_user:
        return {"status": "error", "message": "Username already exists."}, 409

    hash_password = generate_password_hash(data["password"])
    if not create_user(data["username"], hash_password, data["factory"]):
        return {'status': "error", "message": "Failed to create user."}, 500

    return {"status": 'success', "message": 'User created successfully.'}, 201


def user_login_controller(data):
    user = find_user_by_username(data["username"])
    if user and check_password_hash(user["password"], data["password"]):
        access_token = create_access_token(identity=str(user["_id"]), fresh=True)
        refresh_token = create_access_token(identity=str(user["_id"]))
        return {"status": "success", "message": "Login successful.",
                "data": {"access_token": access_token, "refresh_token": refresh_token}}, 200
    return {"status": "error", "message": "Incorrect username or password.", "data": None}, 401


def get_user_controller(user_id):
    user = find_user_by_id(user_id)
    if user:
        user_data = {
            "username": user["username"],
            "factory": user["factory"]
        }
        return {"status": "success", "message": "User retrieved successfully.", "data": user_data}, 200
    return {"status": "error", "message": "User not found.", "data": None}, 404


def user_delete_controller(user_id):
    if delete_user_by_id(user_id):
        return {"status": "success", "message": "User deleted successfully.", "data": None}, 200
    return {"status": "error", "message": "Failed to delete user.", "data": None}, 500
