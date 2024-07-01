from bson import ObjectId
from models import mongo


def create_user(username, password, factory):
    try:
        user_id = mongo.db.users.insert_one({
            "username": username,
            "password": password,
            "factory": factory
        }).inserted_id
        return user_id is not None
    except Exception as e:
        print(f"Failed: {str(e)}")
        return False


def find_user_by_id(user_id):
    try:
        return mongo.db.users.find_one({"_id": ObjectId(user_id)})
    except Exception as e:
        print(f"Failed: {str(e)}")
        return None


def find_user_by_username(username):
    return mongo.db.users.find_one({"username": username})


def delete_user_by_id(user_id):
    try:
        result = mongo.db.users.delete_one({"_id": ObjectId(user_id)})
        return result.deleted_count > 0
    except Exception as e:
        print(f"Failed: {str(e)}")
        return False
