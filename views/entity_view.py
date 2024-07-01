from flask import Blueprint, request, jsonify
from controllers import add_entity_controller, entity_delete_controller, get_entities_controller, get_entity_controller, \
    update_entity_controller
from flask_jwt_extended import jwt_required
from schemas import EntitySchema

entity_bp = Blueprint("entity_bp", __name__)


@entity_bp.route("/entity", methods=["POST"])
@jwt_required()
def add_entity():
    data = request.get_json()
    schema = EntitySchema()
    errors = schema.validate(data)
    if errors:
        return jsonify(errors), 400
    response, status_code = add_entity_controller(data)
    return jsonify(response), status_code


@entity_bp.route("/entities", methods=["GET"])
@jwt_required()
def get_entities():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    response, status_code = get_entities_controller(page, per_page)
    return jsonify(response), status_code


@entity_bp.route("/entity/<string:entity_id>", methods=["GET"])
@jwt_required()
def get_entity(entity_id):
    response, status_code = get_entity_controller(entity_id)
    return jsonify(response), status_code


@entity_bp.route("/entity/<string:entity_id>", methods=["DELETE"])
@jwt_required()
def delete_entity(entity_id):
    response, status_code = entity_delete_controller(entity_id)
    return jsonify(response), status_code


@entity_bp.route("/entity/<string:entity_id>", methods=["PUT"])
@jwt_required()
def update_entity(entity_id):
    data = request.get_json()
    schema = EntitySchema()
    errors = schema.validate(data)
    if errors:
        return jsonify(errors), 400
    response, status_code = update_entity_controller(entity_id, data)
    return jsonify(response), status_code
