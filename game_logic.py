import random

MOVES_DICT = {
    'rock'      : ['scissors', 'lizard'],
    'scissors'  : ['paper', 'lizard'],
    'paper'     : ['rock', 'spock'],
    'lizard'    : ['paper', 'spock'],
    'spock'     : ['rock', 'scissors']
}

class Move():
    def __init__(self):
        self._name = ''

    @property
    def name(self):
        return self._name

    def _set_up_moves_it_can_beat(self, mv1, win_method_1, mv2, win_method_2):
        self._beats = {mv1 : win_method_1,
                       mv2 : win_method_2}

    def win_method(self, opponent_move):
        if opponent_move in self._beats.keys():
            return self._beats[opponent_move]

    def __gt__(self, other):
        if other.name in self._beats:
            return True
        return False
    
    def __lt__(self, other):
        if other.name not in self._beats:
            return True
        return False
    
    def __str__(self):
        return str(self.name)

class Rock(Move):
    def __init__(self):
        super().__init__()
        self._name = 'rock'
        self._set_up_moves_it_can_beat(
            'scissors',
            'Rock smashes Scissors!',
            'lizard',
            'Rock smashes Lizard!'
        )

class Paper(Move):
    def __init__(self):
        super().__init__()
        self._name = 'paper'
        self._set_up_moves_it_can_beat(
            'rock',
            'Paper covers Rock!',
            'spock',
            'Paper disproves Spock!'
        )

class Scissors(Move):
    def __init__(self):
        super().__init__()
        self._name = 'scissors'
        self._set_up_moves_it_can_beat(
            'paper',
            'Scissors cuts Paper!',
            'lizard',
            'Scissors decapitates Lizard!'
        )

class Lizard(Move):
    def __init__(self):
        super().__init__()
        self._name = 'lizard'
        self._set_up_moves_it_can_beat(
            'spock',
            'Lizard poisons Spock!',
            'paper',
            'Lizard eats Paper!'
        )

class Spock(Move):
    def __init__(self):
        super().__init__()
        self._name = 'spock'
        self._set_up_moves_it_can_beat(
            'rock',
            'Spock vapourizes Rock!',
            'scissors',
            'Spock dismantles scissors!'
        )

def determine_winning_move(move1, move2):
    if move2 in MOVES_DICT[move1]:
        return move1
    elif move1 in MOVES_DICT[move2]:
        return move2
    return None

def get_computer_move():
    moves = list(MOVES_DICT.keys())
    return random.choice(moves)

# TESTS
# rock = Rock()
# paper = Paper()
# scissors = Scissors()
# lizard = Lizard()
# spock = Spock()

# print('-----')

# print(rock > lizard)
# print(paper > scissors)
# print(spock > lizard)
# print(paper < scissors)

# print(paper._beats)
# print(paper._beats.keys())
# print(list(paper._beats.keys())[0])
# print(paper.win_method(rock.name))
# print(spock.win_method(rock.name))
# print(lizard.win_method(paper.name))

# TODO:
# Implement moves as a class? To contain winning method, who they beat, etc.