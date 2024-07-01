from flask import Blueprint, request, jsonify
from controllers import add_factory_controller, factory_delete_controller, get_factories_controller, \
    get_factory_controller, update_factory_controller
from schemas import FactorySchema
from flask_jwt_extended import jwt_required

factory_bp = Blueprint("factory_bp", __name__)


@factory_bp.route("/factory", methods=["POST"])
@jwt_required()
def add_factory():
    data = request.get_json()
    schema = FactorySchema()
    errors = schema.validate(data)
    if errors:
        return jsonify(errors), 400
    response, status_code = add_factory_controller(data)
    return jsonify(response), status_code


@factory_bp.route("/factories", methods=["GET"])
@jwt_required()
def get_factories():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    response, status_code = get_factories_controller(page, per_page)
    return jsonify(response), status_code


@factory_bp.route("/factory/<string:factory_id>", methods=["GET"])
@jwt_required()
def get_factory(factory_id):
    response, status_code = get_factory_controller(factory_id)
    return jsonify(response), status_code


@factory_bp.route("/factory/<string:factory_id>", methods=["DELETE"])
@jwt_required()
def factory_delete(factory_id):
    response, status_code = factory_delete_controller(factory_id)
    return jsonify(response), status_code


@factory_bp.route("/factory/<string:factory_id>", methods=["PUT"])
@jwt_required()
def update_factory(factory_id):
    data = request.get_json()
    schema = FactorySchema()
    errors = schema.validate(data)
    if errors:
        return jsonify(errors), 400
    response, status_code = update_factory_controller(factory_id, data)
    return jsonify(response), status_code
