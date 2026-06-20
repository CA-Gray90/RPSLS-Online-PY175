import random

class Player:
    CHOICES = ('rock', 'paper', 'scissors')

    def __init__(self):
        self.move = None

class Computer(Player):
    def __init__(self):
        super().__init__()

    def choose(self):
        self.move = random.choice(Player.CHOICES)

class Human(Player):
    def __init__(self):
        super().__init__()

    def choose(self):
        prompt = "Enter either 'rock', 'paper' or 'scissors'"

        while True:
            move = input(f'{prompt}: ').lower()
            if move in Player.CHOICES:
                break

            print('Invalid input. ', end='')

        self.move = move

class RPSGame:
    def __init__(self):
        self._human = Human()
        self._computer = Computer()

    def _display_welcome_msg(self):
        print('Welcome to Rock Paper Scissors!')

    def _display_goodbye_msg(self):
        print('Thanks for playing Rock Paper Scissors. Goodbye!')

    def _human_wins(self):
        human_move = self._human.move
        computer_move = self._computer.move

        return ((human_move == 'rock' and computer_move == 'scissors') or
            (human_move == 'paper' and computer_move == 'rock') or
            (human_move == 'scissors' and computer_move == 'paper'))

    def _computer_wins(self):
        human_move = self._human.move
        computer_move = self._computer.move

        return ((human_move == 'rock' and computer_move == 'paper') or \
              (human_move == 'paper' and computer_move == 'scissors') or \
              (human_move == 'scissors' and computer_move == 'rock'))

    def _display_winner(self):
        print(f'You chose: {self._human.move.capitalize()}')
        print(f'Computer chose: {self._computer.move.capitalize()}')

        if self._human_wins():
            print('You win!')
        elif self._computer_wins():
            print('Computer won. You lost!')
        else:
            print("It's a Tie!")

    def _play_again(self):
        prompt = 'Play again? (y/n)'

        while True:
            answer = input(f'{prompt}: ').lower()
            if answer in ('yes', 'no', 'y', 'n'):
                return answer[0] == 'y'

            print('Invalid input. ', end='')

    # Orchestration function to play the game
    def play(self):
        self._display_welcome_msg()

        while True:
            self._human.choose()
            self._computer.choose()
            self._display_winner()
            if not self._play_again():
                break

        self._display_goodbye_msg()

RPSGame().play()