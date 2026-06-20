import random

MOVES_DICT = {
    'rock'      : ['scissors', 'lizard'],
    'scissors'  : ['paper', 'lizard'],
    'paper'     : ['rock', 'spock'],
    'lizard'    : ['paper', 'spock'],
    'spock'     : ['rock', 'scissors']
}

def determine_winning_move(move1, move2):
    if move2 in MOVES_DICT[move1]:
        return move1
    elif move1 in MOVES_DICT[move2]:
        return move2
    return None

def get_computer_move():
    moves = list(MOVES_DICT.keys())
    return random.choice(moves)

# Implement moves as a class? To contain winning method, who they beat, etc.