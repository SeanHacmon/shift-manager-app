from models.schedule import users_collection
from bson.objectid import ObjectId

VALID_DAYS = list(range(1, 8))  # 1=Sunday ... 7=Saturday


def validate_schedule_fields(data: dict):
    """
    Validates the structure of a schedule payload.
    Expects: { "schedule": { "EmployeeName": [0, 2, 4], ... }, "manager_id": "..." }
    Returns (True, None) or (False, error_message).
    """
    if 'schedule' not in data or not data['schedule']:
        return False, "Missing required field: 'schedule'"

    if 'manager_id' not in data or not data['manager_id']:
        return False, "Missing required field: 'manager_id'"

    schedule = data['schedule']

    if not isinstance(schedule, dict):
        return False, "'schedule' must be a dictionary mapping employee names to day lists"

    for employee, days in schedule.items():
        if not isinstance(days, list):
            return False, f"Days for '{employee}' must be a list"

        invalid_days = [d for d in days if d not in VALID_DAYS]
        if invalid_days:
            return False, f"Invalid days for '{employee}': {invalid_days}. Use 0 (Sun) - 6 (Sat)"

        if len(days) != len(set(days)):
            return False, f"Duplicate days found for '{employee}'"

    return True, None


def validate_manager_exists(manager_id: str):
    """
    Checks that the given ID belongs to a user with role 'manager'.
    Returns (manager_doc, None) or (None, error_message).
    """
    try:
        obj_id = ObjectId(manager_id)
    except Exception:
        return None, f"Invalid manager ID format: '{manager_id}'"

    manager = users_collection.find_one({'_id': obj_id, 'role': 'manager'})
    if not manager:
        return None, f"No manager found with ID '{manager_id}'"

    return manager, None


def validate_schedule_exists_for_manager(manager_id: str):
    """
    Checks that the manager has a saved schedule.
    Returns (manager_doc, None) or (None, error_message).
    """
    try:
        obj_id = ObjectId(manager_id)
    except Exception:
        return None, f"Invalid manager ID format: '{manager_id}'"

    manager = users_collection.find_one({'_id': obj_id, 'schedule': {'$exists': True}})
    if not manager:
        return None, f"No schedule found for manager ID '{manager_id}'"

    return manager, None