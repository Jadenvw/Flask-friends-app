from flask import Blueprint, request, jsonify
import logging
from extensions import limiter
from werkzeug.security import generate_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity
from user.repo import remove_user, get_user_by_id
from user.service import register_user_service, UserAlreadyExists, RegistrationValidationError 
from user.service import delete_user_service, InvalidIdentity, UserNotFound


user_bp = Blueprint("user", __name__)
logger = logging.getLogger(__name__)


@user_bp.post("/api/user/register")
@limiter.limit("5 per minute")
def register_user():
    logger.info("HIT REGISTER ROUTE")
    # request is not JSON -> 400
    if not request.is_json:
        return jsonify({"error": "Requests must be JSON"}), 400
    
    data = request.get_json()
    # no data -> 400
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400
    
    # parse data from JSON
    username, password = data.get("username"), data.get("password")
    try:    
        user_row = register_user_service(username, password)
        
        # return validation response -> 201
        return jsonify({"id": user_row["id"], "username": user_row["username"]}), 201
    except RegistrationValidationError as e:
        return jsonify({"errors": e.errors}), 400
    except UserAlreadyExists:
        return jsonify({"error": "Username already exists"}),
    

@user_bp.post("/api/user/delete")
@jwt_required()
def delete_user():
    identity = get_jwt_identity()
    try:
        delete_user_service(identity)
        return "", 204
    except InvalidIdentity:
        return jsonify({"error": "Unauthorized"}), 401
    except UserNotFound:
        return jsonify({"error": "User not found"}), 404