def validate_data(data):
    errors = []

    # Name validation
    if not data.get("name"):
        errors.append("Name missing")
    elif len(data["name"]) < 3:
        errors.append("Name too short")

    # Amount validation
    if not data.get("amount"):
        errors.append("Amount missing")
    else:
        try:
            val = float(data["amount"])
            if val <= 0: errors.append("Amount must be positive")
        except ValueError:
            errors.append("Invalid amount format")

    # Date validation
    if not data.get("date"):
        errors.append("Date missing")

    # ID validation
    if not data.get("id"):
        errors.append("Identification (ID/Invoice) missing")

    return {
        "is_valid": len(errors) == 0,
        "errors": errors
    }
