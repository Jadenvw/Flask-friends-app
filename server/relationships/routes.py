from flask import Blueprint, jsonify, request
import logging
from extensions import limiter
from flask_jwt_extended import jwt_required, get_jwt_identity
# from relationships.helpers import canonical_pair
from relationships.repo import find_relationship, insert_pending_relationship
from user.repo import get_user_by_id

relationshp_bp = Blueprint("friend", __name__)
logger = logging.getLogger(__name__)

@relationshp_bp.post("/api/friend/request")
@jwt_required()
@limiter.limit("3 per minute")
def send_friend_request():
    try:
        sender_id = int(get_jwt_identity())

        if not request.is_json:
            return jsonify({"error": "Request must be JSON."}), 400
        
        data = request.get_json()

        if not data:
            return jsonify({"error": "Invalid JSON request."}), 400
        
        target_id = data.get("target_id")

        if not target_id:
            return jsonify({"error": "Invlaid JSON request."}), 400
        
        if sender_id == target_id:
            return jsonify({"error": "Invalid JSON request."}), 409
        
        if not get_user_by_id(target_id):
            return jsonify({"error": "Target user does not exist."}), 404
        
        # pair_low, pair_high = canonical_pair(sender_id, target_id)
        
        relationship = find_relationship(sender_id, target_id)
        if relationship:
            if relationship["relationship_status"] == "blocked":
                return jsonify({"error": "The relationship has been blocked."}), 403
            elif relationship["relationship_status"] == "accepted":
                return jsonify({"error": "Users are already friends."}), 409
            else:
                return jsonify({"error": "Pending request already exists."}), 409
                
        
        row = insert_pending_relationship(sender_id, target_id)
        print(type(row))
        return jsonify(
            {"id": row["id"], 
             "sender": sender_id, 
             "target": target_id, 
             "status": row["relationship_status"], 
             "created_at": row["created_at"]}
            ), 201
        
    except Exception as e:
        logger.error(str(e))
        return jsonify({"error": "Internal Server Error"}), 500