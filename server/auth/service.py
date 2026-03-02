"""
Auth Service Layer:
    - Contains business logic for authentication-related operations.
    - Keeps HTTP parsing and response construction in the routes module.

Responsibilities:
    - Validate credentials and identities.
    - Coordinate repository calls to fetch user data.

This layer must not:
    - Directly interact with Flask request/response objects.
    - Contain SQL statements (delegated to repositories).
"""

from werkzeug.security import check_password_hash
from user.repo import get_user_by_id, get_user_by_username

USERNAME_MIN = 3
USERNAME_MAX = 8


class LoginValidationError(Exception):
    def __init__(self, errors: dict[str, str]):
        super().__init__("Login validation failed")
        self.errors = errors


class InvalidCredentials(Exception):
    pass


class UserNotFound(Exception):
    pass


class InvalidIdentity(Exception):
    pass


def authenticate_user_service(username: str | None, password: str | None):
    errors: dict[str, str] = {}

    if not username:
        errors["username"] = "Username is required."
    elif len(username) < USERNAME_MIN or len(username) > USERNAME_MAX:
        errors["username"] = f"Username must be {USERNAME_MIN}-{USERNAME_MAX} characters long."

    if not password:
        errors["password"] = "Password is required."

    if errors:
        raise LoginValidationError(errors)

    user_row = get_user_by_username(username)
    if not user_row:
        raise UserNotFound()

    if not check_password_hash(user_row["password_hash"], password):
        raise InvalidCredentials()

    return user_row


def get_current_user_service(identity: str):
    try:
        user_id = int(identity)
    except (ValueError, TypeError):
        raise InvalidIdentity()

    user_row = get_user_by_id(user_id)
    if not user_row:
        raise UserNotFound()

    return user_row
