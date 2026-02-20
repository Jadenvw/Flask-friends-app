from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
import re
from auth.repo import create_user
import sqlite3
import logging
from extensions import limiter

auth_bp = Blueprint("auth", __name__)
logger = logging.getLogger(__name__)
PATTERN_RE = re.compile(r'^(?=\S{8,}$)(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).*$')

"""
Build register in three layers:
1) Route parses request + validates input
2) Service logic handles business rules
3) DB layer inserts user
"""
@auth_bp.post("/api/auth/register")
@limiter.limit("1 per minute")
def register():
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

        response = create_user(username, password_hash)
        # return validation response -> 201
        return jsonify(response), 201
    
    except sqlite3.IntegrityError as e:
        logger.error("IntegrityError during register: %s", e)
        # use containment so you don't rely on exact strings
        if "UNIQUE constraint failed: users.username" in str(e):
            return jsonify({"error": "Username already exists"}), 409
        else:
            return jsonify({"error": "Error saving user to database"}), 400
    except Exception as e:
        print(str(e))
        return jsonify({"error": "Server error"}), 500
    

        
        
    




