"""
User Service Layer:
    - This module contains business logic and workflow orchestration for user-related operations.
    - The service layer represents the boundary between HTTP-facing routes and database-facing repositories.

Responsibilities:
    - Enforce business rules.
    - Coordinate multiple repository calls.
    - Define transaction boundaries (commit/rollback).
    - Translate low-level database errors into domain-specific exceptions.

This layer must not:
    - Perform HTTP request parsing.
    - Return Flask response objects.
    - Contain direct SQL statements.  
"""

# user/service.py
import sqlite3
from werkzeug.security import generate_password_hash
from db import get_db
from user.repo import insert_user, get_user_by_id, remove_user
import re

USERNAME_MIN = 3
USERNAME_MAX = 8
PASSWORD_PATTERN = re.compile(r'^(?=\S{8,}$)(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).*$')

class UserAlreadyExists(Exception):
    pass

class RegistrationValidationError(Exception):
    """Exception raised for errors in the registration form."""

    def __init__(self, errors: dict[str, str]) -> None:
        super().__init__("Registration validation failed")
        self.errors = errors

    def __str__(self) -> str:
        return f"{self.field}: {self.message}"

class InvalidCredentials(Exception):
    pass

class UserNotFound(Exception):
    pass

class InvalidIdentity(Exception):
    pass

def register_user_service(username: str, password: str) -> sqlite3.Row:
    conn = get_db()
    errors: dict[str, str] = {}

    if not username:
        errors["username"] = "Username is required."
    elif len(username) < USERNAME_MIN or len(username) > USERNAME_MAX:
        errors["username"] = f"Username must be {USERNAME_MIN}–{USERNAME_MAX} characters long."
    
    if not password:
        errors["password"] = "Password is required." 
    elif not PASSWORD_PATTERN.match(password):
        errors["password"] = "Password must be at least 8 characters and include an uppercase letter, a number, and a special character."
    
    if errors:
        raise RegistrationValidationError(errors)
    
    password_hash = generate_password_hash(password)

    try:
        user_row = insert_user(username, password_hash)
        conn.commit()
        return user_row
    except sqlite3.IntegrityError as e:
        conn.rollback()
        if "UNIQUE constraint failed: users.username" in str(e):
            raise UserAlreadyExists()
        raise
    except Exception:
        conn.rollback()
        raise

def delete_user_service(identity: str) -> None:
    conn = get_db()
    try:
        user_id = int(identity)
    except (ValueError, TypeError):
        raise InvalidIdentity()
        
    user_row = get_user_by_id(user_id)

    if not user_row:
        raise UserNotFound()
    try:
        remove_user(user_id)
        conn.commit()
    except Exception:
        conn.rollback()
        raise
        
    
