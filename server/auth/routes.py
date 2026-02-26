from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, set_access_cookies, jwt_required, get_jwt_identity, unset_jwt_cookies
from user.repo import get_user_by_username
import logging
from extensions import limiter
from db import get_db

auth_bp = Blueprint("auth", __name__)
logger = logging.getLogger(__name__)


@auth_bp.get("/api/auth/me")
@jwt_required()
def me():
    try:
        user_id = int(get_jwt_identity())
        print(type(user_id))
        return jsonify({"user_id": user_id}), 200
    except Exception as e:
        logger.error(str(e))
        return jsonify({"error": "Internal Sever Error"}), 500
    

@auth_bp.post("/api/auth/login")
@limiter.limit("3 per minute")
def login():
    conn = get_db()
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
        
        # parse JSON
        username, password = data.get("username"), data.get("password")

        # check we have required fields
        if not username:
            logger.error("Error username required")
            return jsonify({"error": "Error username required"}), 400
        
        if not password:
            logger.error("Error password required")
            return jsonify({"error": "Error password required"}), 400

        # verify the username could exist
        if len(username) < 3 or len(username) > 8:
            logger.error("Invalid credentials.")
            return jsonify({"error": "Invalid credentials."}), 401
        
        # get user row from the DB
        user = get_user_by_username(conn, username)

        if not user:
            logger.error("User not found.")
            return jsonify({"error": "User not found."}), 404
        
        password_hash = user["password_hash"]
        # check password
        if not check_password_hash(password_hash, password):
            logger.error("Invalid credentials.")
            return jsonify({"error": "Invalid credentials."}), 401
        
        # token creation
        access_token = create_access_token(identity=str(user["id"]))
        response = jsonify(msg="login successful")
        set_access_cookies(response, access_token)
        return response, 200
        
    except Exception as e:
        logger.error(str(e))
        return jsonify({"error": "Internal Server Error"}), 500
    

@auth_bp.post("/api/auth/logout")
def logout():
    response = jsonify(msg="logout successful")
    unset_jwt_cookies(response)
    return response, 200

        
    




