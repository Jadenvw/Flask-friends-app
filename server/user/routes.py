from flask import Blueprint, request, jsonify
import sqlite3
import logging
from extensions import limiter
from werkzeug.security import generate_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity
import re
from user.repo import insert_user, delete_user, get_user_by_id

user_bp = Blueprint("user", __name__)
logger = logging.getLogger(__name__)
PATTERN_RE = re.compile(r'^(?=\S{8,}$)(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).*$')

"""
Build register in three layers:
1) Route parses request + validates input
2) Service logic handles business rules
3) DB layer inserts user
"""
@user_bp.post("/api/user/register")
@limiter.limit("5 per minute")
def create_user():
    logger.info("HIT REGISTER ROUTE")
    try:
        # request is not JSON -> 400
        if not request.is_json:
            return jsonify({"error": "Requests must be JSON"}), 400
        
        data = request.get_json()
        
        # no data -> 400
        if not data:
            return jsonify({"error": "Invalid JSON"}), 400
        
        # parse data
        username, password = data.get("username"), data.get("password")
        
        # validation checks -> 400
        if not username:
            return jsonify({"error": "Error username required"}), 400
        
        if not password:
            return jsonify({"error": "Error password required"}), 400
        
        if len(username) < 3 or len(username) > 8:
            return jsonify({"error": "Invalid username"}), 400
        
        if not PATTERN_RE.match(password):
            return jsonify({"error": "Invalid password"}), 400
        
        # Generate hashed password w/ werkzeug
        password_hash = generate_password_hash(password)

        response = insert_user(username, password_hash)
        logger.info("Inserted user")
        
        # return validation response -> 201
        return jsonify({"id": response["id"], "username": response["username"]}), 201
    except sqlite3.IntegrityError as e:
        logger.error("IntegrityError while creating user: %s", e)
        # use containment so you don't rely on exact strings
        if "UNIQUE constraint failed: users.username" in str(e):
            return jsonify({"error": "Username already exists"}), 409
        else:
            return jsonify({"error": "Error saving user to database"}), 400
    except Exception as e:
        logger.error(str(e))
        return jsonify({"error": "Server error"}), 500
    

@user_bp.post("/api/user/delete")
@jwt_required()
def delete_user():
    try:
        id = int(get_jwt_identity())
        
        user = get_user_by_id(id)
       
        if not user:
            return jsonify({"error": "User not found"}), 404

        response = delete_user(id)
        
        return jsonify(response), 204
    
    except Exception as e:
        logger.error(str(e))
        return jsonify({"error": "Interal Server Error"}), 500