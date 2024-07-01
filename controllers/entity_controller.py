from models.entity_model import add_entity, find_entities, find_entity_by_id, update_entity, delete_entity_by_id


def add_entity_controller(data):
    if not add_entity(data['name'], data['factory']):
        return {"status": "error", "message": "Failed to create entity.", "data": None}, 500
    return {"status": "success", "message": "Entity created successfully.", "data": None}, 200


def get_entities_controller(page, per_page):
    entities = find_entities(page, per_page)
    if entities:
        return {"status": "success", "message": "Entities retrieved successfully.", "data": entities}, 200
    return {"status": "error", "message": "No entities found.", "data": None}, 404


def get_entity_controller(entity_id):
    entity = find_entity_by_id(entity_id)
    if entity:
        entity_data = {
            "name": entity["name"],
            "factory": entity["factory"]
        }
        return {"status": "success", "message": "Entity retrieved successfully.", "data": entity_data}, 200
    return {"status": "error", "message": "Entity not found.", "data": None}, 404


def update_entity_controller(entity_id, data):
    if update_entity(entity_id, data["name"], data["factory"]):
        return {"status": "success", "message": "Entity updated successfully.", "data": None}, 200
    return {"status": "error", "message": "Failed to update entity.", "data": None}, 500


def entity_delete_controller(entity_id):
    if delete_entity_by_id(entity_id):
        return {"status": "success", "message": "Entity deleted successfully.", "data": None}, 200
    return {"status": "error", "message": "Failed to delete entity.", "data": None}, 500
