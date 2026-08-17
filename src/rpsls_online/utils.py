import yaml, re

def valid_player_name(name):
    if re.search(r'\W', name):
        print('Invalid name')
        return False
    return True

def include_score_in_leaderboard(score, leaderboard):
    if len(leaderboard) < 5:
        return True
    return any(score >= other_score for _, other_score in leaderboard)

def get_leaderboard(file_path):
    with open(file_path, 'r') as file:
            leaderboard = [(name, score) for name, score in yaml.safe_load(file).items()]
            leaderboard.sort(key=lambda tup: tup[1], reverse=True)

    return leaderboard