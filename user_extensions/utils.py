def split_full_name(full_name):
    """
    Split a full name into its constituent parts: first name, middle name (if exists) and last name.

    Args:
        full_name (str): Full name to be split.

    Returns:
        tuple: Tuple containing the first name, middle name, and last name (in that order).
    """
    name_parts = full_name.split()

    first_name = name_parts[0]
    middle_name = " ".join(name_parts[1:-1]) if len(name_parts) > 2 else ''
    last_name = name_parts[-1] if len(name_parts) >= 2 else ''

    return first_name, middle_name, last_name