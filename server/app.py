from flask import Flask, jsonify
from flask_cors import CORS
import logging
from extensions import limiter
from flask_limiter.errors import RateLimitExceeded
from db import close_db
from dotenv import load_dotenv
import os
from flask_jwt_extended import JWTManager
from datetime import timedelta

# reads .env, parses it, inserts key=value pairs into os.environ
load_dotenv()

# application factory
def create_app():
    # Creates web application obj
    app = Flask(__name__)

    # configures global logging around the app
    """
    logging:
    - DEBUG: very detailed internal state. Only useful when debugging
    - INFO: Normal operation event. Something happens as expected
    - WARNING: Something suspicious but not broken: singals potential abuse
    - ERROR: Something broke but app continues
    - CRITICAL: the app is dying: usually precedes shutdown
    """
    logging.basicConfig(level=logging.INFO)

    app.teardown_appcontext(close_db)

    # retrieve JWT from os
    secret = os.environ.get("JWT_SECRET_KEY")
    # Check if the secret exists
    if not secret:
        # failure
        raise RuntimeError("JWT_SECRET_KEY is not set")
    # store JWT in Flask config
    app.config["JWT_SECRET_KEY"] = secret
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=30)
    logging.info("JWT_SECRET_KEY configured.")
    # wire JWT into Flask
    JWTManager(app)

    # create a global limiter for the app
    limiter.init_app(app)
    # handle any instance where a rate limit is hit
    @app.errorhandler(RateLimitExceeded)
    def handle_rate_limit(e):
        return jsonify({"error": "Too many requests. Try again later."}), 429
    
    # frontend runs on diff origin (diff port); Browsers bloack cross-origin requests unless we allow it
    # requests from react are allowed for all api routes
    # CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})
    CORS(app) # this allows requests from any origin to any route

    from auth.routes import auth_bp
    app.register_blueprint(auth_bp)
    from user.routes import user_bp
    app.register_blueprint(user_bp)
    from relationships.routes import relationshp_bp
    app.register_blueprint(relationshp_bp)

    # defines route for sanity endpoint
    @app.get("/api/health")
    def health():
        # jsonify returns proper JSON w/ headers
        return jsonify({"ok": True})
    
    @app.get("/api/limit-test")
    @limiter.limit("3 per minute")
    def limit_test():
        return jsonify({"ok": True}), 200
    
    
    return app


if __name__ == "__main__":
    app = create_app()
    # runs dev server on port 5000 w/ auto-reload 
    app.run(debug=True, port=5000)