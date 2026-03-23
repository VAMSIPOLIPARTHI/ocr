def trigger_action(data, validation):
    """
    Generalized action trigger based on validation results.
    Triggers automated processing for valid documents or manual review for invalid ones.
    """
    if not validation["is_valid"]:
        return "Action: Manual Review Required - Document failed validation rules"

    return "Action: Automated Processing & Integration Triggered"


