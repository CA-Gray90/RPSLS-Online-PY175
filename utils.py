def valid_player_name(name, allowed_length):
    if not name or len(name) > allowed_length:
        return False
    return True

def update_leaderboard(player_name, score, leaderboard):
    if len(leaderboard) < 5:
        leaderboard.append((player_name, score))
    elif include_score_in_leaderboard(score, leaderboard):
        leaderboard.pop()
        leaderboard.append((player_name, score))

    return leaderboard

def include_score_in_leaderboard(score, leaderboard):
    if len(leaderboard) < 5:
        return True
    return any(score >= other_score for _, other_score in leaderboard)

def leaderboard_dict_to_sorted_list(leaderboard_dict):
    leaderboard = [(name, score) for name, score in leaderboard_dict.items()]
    return sorted(leaderboard, key=lambda tup: (-tup[1], tup[0]))