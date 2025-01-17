import os

from flask import Flask, jsonify
from views import user_bp, factory_bp, entity_bp
from models import mongo
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

from blocklist import BLOCKLIST


def create_app():
    app = Flask(__name__)
    load_dotenv()

    app.config['MONGO_URI'] = os.getenv("MONGO_URI")
    app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")

    jwt = JWTManager(app)
    mongo.init_app(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        jti = jwt_payload["jti"]
        return jti in BLOCKLIST

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {"description": "The token has been revoked.", "error": "token_revoked"}
            ),
            401,
        )

    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {
                    "description": "The token is not fresh.",
                    "error": "fresh_token_required",
                }
            ),
            401,
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "description": "Request does not contain an access token.",
                    "error": "authorization_required",
                }
            ),
            401,
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
                {"message": "Signature verification failed.", "error": "invalid_token"}
            ),
            401,
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "description": "Request does not contain an access token.",
                    "error": "authorization_required",
                }
            ),
            401,
        )

    app.register_blueprint(user_bp)
    app.register_blueprint(factory_bp)
    app.register_blueprint(entity_bp)
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
