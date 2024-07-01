from flask import Blueprint, request, jsonify
from controllers.user_controller import user_register_controller, user_login_controller, get_user_controller, \
    user_delete_controller
from schemas.user_schema import UserRegisterSchema, UserSchema
from flask_jwt_extended import jwt_required, get_jwt, create_access_token, get_jwt_identity
from blocklist import BLOCKLIST

user_bp = Blueprint("user_bp", __name__)


@user_bp.route("/register", methods=["POST"])
def user_register():
    data = request.get_json()
    schema = UserRegisterSchema()
    errors = schema.validate(data)
    if errors:
        return jsonify(errors), 400
    response, status_code = user_register_controller(data)
    return jsonify(response), status_code


@user_bp.route("/login", methods=["POST"])
def user_login():
    data = request.get_json()
    schema = UserSchema()
    errors = schema.validate(data)
    if errors:
        return jsonify(errors), 400
    response, status_code = user_login_controller(data)
    return jsonify(response), status_code


@user_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def token_refresh():
    identity = get_jwt_identity()
    new_access_token = create_access_token(identity=identity, fresh=False)
    return jsonify({"access_token": new_access_token}), 200


@user_bp.route("/logout", methods=["POST"])
@jwt_required()
def user_logout():
    jti = get_jwt()["jti"]
    BLOCKLIST.add(jti)
    return jsonify({"msg": "Successfully logged out"}), 200


@user_bp.route("/user/<string:user_id>", methods=["GET"])
@jwt_required()
def get_user(user_id):
    response, status_code = get_user_controller(user_id)
    return jsonify(response), status_code


@user_bp.route("/user/<string:user_id>", methods=["DELETE"])
@jwt_required()
def delete_user(user_id):
    response, status_code = user_delete_controller(user_id)
    return jsonify(response), status_code
