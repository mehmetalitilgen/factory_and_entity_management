from models import mongo
from bson import ObjectId


def create_factory(name, location, capacity):
    try:
        factory_id = mongo.db.factories.insert_one({
            "name": name,
            "location": location,
            "capacity": capacity
        }).inserted_id
        return factory_id is not None
    except Exception as e:
        print(f"Failed: {str(e)}")
        return False


def find_factories(page, per_page):
    try:
        factories = mongo.db.factories.find().skip((page - 1) * per_page).limit(per_page)
        factory_list = []
        for factory in factories:
            factory['_id'] = str(factory['_id'])
            factory_list.append(factory)
        return factory_list
    except Exception as e:
        print(f"Failed: {str(e)}")
        return []


def find_factory_by_id(factory_id):
    try:
        factory = mongo.db.factories.find_one({"_id": ObjectId(factory_id)})
        if factory:
            factory['_id'] = str(factory['_id'])
        return factory
    except Exception as e:
        print(f"Failed: {str(e)}")
        return None


def delete_factory_by_id(factory_id):
    try:
        result = mongo.db.factories.delete_one({"_id": ObjectId(factory_id)})
        return result.deleted_count > 0
    except Exception as e:
        print(f"Failed: {str(e)}")
        return False


def find_factory_by_name(name):
    return mongo.db.factories.find_one({"name": name})


def update_factory(factory_id, name, location, capacity):
    try:
        result = mongo.db.factories.update_one(
            {"_id": ObjectId(factory_id)},
            {"$set": {"name": name, "location": location, "capacity": capacity}}
        )
        return result.modified_count > 0
    except Exception as e:
        print(f"Failed: {str(e)}")
        return False
