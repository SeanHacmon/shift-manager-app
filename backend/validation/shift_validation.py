VALID_DAYS = list(range(1, 8))  # 1=Sunday ... 7=Saturday


def validate_availability(availability: list):
    """
    Validates a user's availability list.
    Rules:
      - Must be a non-empty list
      - Cannot contain more than 7 days
      - All values must be integers between 1 and 7 (inclusive)
      - No duplicate days allowed
    Returns (True, None) or (False, error_message).
    """
    if not isinstance(availability, list) or len(availability) == 0:
        return False, "'availability' must be a non-empty list"

    if len(availability) > 7:
        return False, f"'availability' cannot contain more than 7 days, got {len(availability)}"

    if len(availability) != len(set(availability)):
        return False, "'availability' cannot contain duplicate days"

    for day in availability:
        if not isinstance(day, int):
            return False, f"All values in 'availability' must be integers, got '{day}'"
        if day not in VALID_DAYS:
            return False, f"Invalid day '{day}'. Values must be between 1 (Sun) and 7 (Sat)"

    return True, None