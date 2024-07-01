from models.factory_model import create_factory, find_factories, find_factory_by_id, delete_factory_by_id, \
    update_factory


def add_factory_controller(data):
    if not create_factory(data['name'], data['location'], data['capacity']):
        return {"status": "error", "message": "Failed to create factory.", "data": None}, 500
    return {"status": "success", "message": "Factory created successfully.", "data": None}, 200


def get_factories_controller(page, per_page):
    factories = find_factories(page, per_page)
    if factories:
        return {"status": "success", "message": "Factories retrieved successfully.", "data": factories}, 200
    return {"status": "error", "message": "No factories found.", "data": None}, 404


def get_factory_controller(factory_id):
    factory = find_factory_by_id(factory_id)
    if factory:
        factory_data = {
            "name": factory["name"],
            "location": factory["location"],
            "capacity": factory["capacity"]
        }
        return {"status": "success", "message": "Factory retrieved successfully.", "data": factory_data}, 200
    return {"status": "error", "message": "Factory not found.", "data": None}, 404


def update_factory_controller(factory_id, data):
    if update_factory(factory_id, data["name"], data["location"], data["capacity"]):
        return {"status": "success", "message": "Factory updated successfully.", "data": None}, 200
    return {"status": "error", "message": "Failed to update factory.", "data": None}, 500


def factory_delete_controller(factory_id):
    if delete_factory_by_id(factory_id):
        return {"status": "success", "message": "Factory deleted successfully.", "data": None}, 200
    return {"status": "error", "message": "Failed to delete factory.", "data": None}, 500
