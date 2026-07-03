import random

MOVES = ['scissors', 'paper', 'rock', 'lizard', 'spock']

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

def string_to_move_object(string_move):
    if string_move not in MOVES:
        return None
    
    string_move = string_move.lower()
    for move in [Rock, Paper, Scissors, Lizard, Spock]:
        move_obj = move()
        if move_obj.name == string_move:
            return move_obj

def determine_winning_move(move1, move2):
    print(f'move1 : {move1}, move2 : {move2}')
    move1 = string_to_move_object(move1)
    move2 = string_to_move_object(move2)
    print(f'move1 : {move1}, move2 : {move2}')
    
    if move1 > move2:
        return move1.name
    elif move2 > move1:
        return move2.name
    return None

def get_computer_move():
    return random.choice(MOVES)


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