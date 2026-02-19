from models.user import users_collection
from bson.objectid import ObjectId

VALID_DEPARTMENTS = ['Bartender', 'Waiter']
VALID_ROLES = ['manager', 'employee']
VALID_DAYS = list(range(1, 8))  # 1=Sunday ... 7=Saturday


def validate_user_exists_by_email(email: str):
    """
    Returns (user_doc, error_message).
    If user is found, error_message is None.
    If not found, user_doc is None.
    """
    user = users_collection.find_one({'email': email})
    if not user:
        return None, f"No user found with email '{email}'"
    return user, None


def validate_user_exists_by_id(user_id: str):
    """
    Returns (user_doc, error_message).
    Validates that the ID is a valid ObjectId format before querying.
    """
    try:
        obj_id = ObjectId(user_id)
    except Exception:
        return None, f"Invalid user ID format: '{user_id}'"

    user = users_collection.find_one({'_id': obj_id})
    if not user:
        return None, f"No user found with ID '{user_id}'"
    return user, None


def validate_user_not_exists(email: str):
    """
    Ensures a user does NOT already exist (useful for registration).
    Returns (True, None) if email is free, or (False, error_message) if taken.
    """
    user = users_collection.find_one({'email': email})
    if user:
        return False, f"A user with email '{email}' already exists"
    return True, None


def validate_registration_fields(data: dict):
    """
    Validates all required fields for creating a new user.
    Returns (True, None) on success, or (False, error_message) on failure.
    """
    required = ['firstName', 'lastName', 'email', 'password', 'department', 'availableDays']

    for field in required:
        if field not in data or not data[field]:
            return False, f"Missing required field: '{field}'"

    if not isinstance(data['availableDays'], list):
        return False, "'availableDays' must be a list"

    invalid_days = [d for d in data['availableDays'] if d not in VALID_DAYS]
    if invalid_days:
        return False, f"Invalid days in 'availableDays': {invalid_days}. Use 0 (Sun) - 6 (Sat)"

    if data.get('department') not in VALID_DEPARTMENTS:
        return False, f"Invalid department. Choose from: {VALID_DEPARTMENTS}"

    if 'role' in data and data['role'] not in VALID_ROLES:
        return False, f"Invalid role. Choose from: {VALID_ROLES}"

    if '@' not in data['email'] or '.' not in data['email']:
        return False, "Invalid email format"

    if len(data['password']) < 6:
        return False, "Password must be at least 6 characters"

    return True, None


def validate_login_fields(data: dict):
    """
    Validates fields required for login.
    Returns (True, None) or (False, error_message).
    """
    for field in ['email', 'password']:
        if field not in data or not data[field]:
            return False, f"Missing required field: '{field}'"
    return True, None