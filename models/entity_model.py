from models import mongo
from bson import ObjectId


def add_entity(name, factory):
    try:
        entity_id = mongo.db.entities.insert_one({
            "name": name,
            "factory": factory
        }).inserted_id
        return entity_id is not None
    except Exception as e:
        print(f"Failed: {str(e)}")
        return False


def find_entities(page, per_page):
    try:
        entities = mongo.db.entities.find().skip((page - 1) * per_page).limit(per_page)
        entity_list = []
        for entity in entities:
            entity['_id'] = str(entity['_id'])
            entity_list.append(entity)
        return entity_list
    except Exception as e:
        print(f"Failed: {str(e)}")
        return []


def find_entity_by_id(entity_id):
    try:
        entity = mongo.db.entities.find_one({"_id": ObjectId(entity_id)})
        if entity:
            entity['_id'] = str(entity['_id'])
        return entity
    except Exception as e:
        print(f"Failed: {str(e)}")
        return None


def delete_entity_by_id(entity_id):
    try:
        result = mongo.db.entities.delete_one({"_id": ObjectId(entity_id)})
        return result.deleted_count > 0
    except Exception as e:
        print(f"Failed: {str(e)}")
        return False


def find_entity_by_name(name):
    return mongo.db.entities.find_one({"name": name})


def update_entity(entity_id, name, factory):
    try:
        result = mongo.db.entities.update_one(
            {"_id": ObjectId(entity_id)},
            {"$set": {"name": name, "factory": factory}}
        )
        return result.modified_count > 0
    except Exception as e:
        print(f"Failed: {str(e)}")
        return False
