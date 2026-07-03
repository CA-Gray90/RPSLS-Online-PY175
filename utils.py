def valid_player_name(name, allowed_length):
    # Checks for basic validations
    if not name or len(name) > allowed_length:
        return False
    return True
    