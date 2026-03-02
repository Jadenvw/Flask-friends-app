from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, set_access_cookies, jwt_required, get_jwt_identity, unset_jwt_cookies
import logging
from extensions import limiter
from auth.service import (
    authenticate_user_service,
    get_current_user_service,
    LoginValidationError,
    InvalidCredentials,
    UserNotFound,
    InvalidIdentity,
)

auth_bp = Blueprint("auth", __name__)
logger = logging.getLogger(__name__)


@auth_bp.get("/api/auth/me")
@jwt_required()
def me():
    identity = get_jwt_identity()
    try:
        user_row = get_current_user_service(identity)
        return jsonify({
            "user": {
                "id": user_row["id"],
                "username": user_row["username"],
            }
        }), 200
    except (InvalidIdentity, UserNotFound):
        return jsonify({"error": "Unauthorized"}), 401
    

@auth_bp.post("/api/auth/login")
@limiter.limit("3 per minute")
def login():
    try:
        # check that request is JSON
        if not request.is_json:
            logger.error("Requests must be JSON")
            return jsonify({"error": "Requests must be JSON"}), 400
        
        # store request in data var
        data = request.get_json()

        # check that the JSON is not empty
        if not data:
            logger.error("Missing required fields")
            return jsonify({"error": "Missing required fields"}), 400
        
        username, password = data.get("username"), data.get("password")
        user_row = authenticate_user_service(username, password)

        access_token = create_access_token(identity=str(user_row["id"]))
        response = jsonify(msg="login successful")
        set_access_cookies(response, access_token)
        return response, 200
    except LoginValidationError as e:
        return jsonify({"errors": e.errors}), 400
    except UserNotFound:
        return jsonify({"error": "User not found."}), 404
    except InvalidCredentials:
        return jsonify({"error": "Invalid credentials."}), 401
    except Exception as e:
        logger.error(str(e))
        return jsonify({"error": "Internal Server Error"}), 500
    

@auth_bp.post("/api/auth/logout")
def logout():
    response = jsonify(msg="logout successful")
    unset_jwt_cookies(response)
    return response, 200

        
    


