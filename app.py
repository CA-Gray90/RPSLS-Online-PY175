from src.rpsls_online.database_persistence import DatabasePersistence

from flask import (
    Flask,
    flash,
    g,
    render_template,
    redirect,
    request,
    session,
    url_for
    )

from src.rpsls_online.game_logic import (
    get_computer_move,
    get_winning_method,
    determine_winning_move)

import os, secrets, src.rpsls_online.utils, yaml
from functools import wraps

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

MAX_PLAYERNAME_LENGTH = 10
MAX_ROUNDS_PER_GAME = 5

def requires_playername(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not session.get('player_name', None):
            return redirect(url_for('enter_playername'))
        else:
            return func(*args, **kwargs)

    return wrapper

@app.before_request
def get_data_path():
    root = os.path.abspath(os.path.dirname(__file__))
    g.data_dir = os.path.join(root, 'rpsls_online', 'data')
    g.leaderboard_storage = DatabasePersistence()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/rules')
def display_rules():
    with open(os.path.join(g.data_dir, 'rules.yaml'), 'r') as file:
        rules = yaml.safe_load(file)

    return render_template('rules.html',
                           opening_lines=rules['opening_lines'],
                           game_actions=rules['game_actions'])

@app.route('/leaderboard')
def display_leaderboard():
    leaderboard = g.leaderboard_storage.get_leaderboard()
    return render_template('leaderboard.html', leaderboard=leaderboard)

@app.route('/enter_playername')
def enter_playername():
    return render_template('pick_playername.html',
                           max_playername_length=MAX_PLAYERNAME_LENGTH)

@app.route('/enter_playername/validate', methods=['POST'])
def validate_playername():
    player_name = request.form['player_name'].strip()

    if not src.rpsls_online.utils.valid_player_name(player_name):
        flash('Not a valid username. Use only numbers and letters. Try again.',
              'error')
        return render_template('pick_playername.html',
                               current_name=player_name,
                               max_playername_length=MAX_PLAYERNAME_LENGTH)

    leaderboard = g.leaderboard_storage.get_leaderboard()

    if player_name in dict(leaderboard).keys():
        flash('Please choose another username, current one in leaderboard.',
              'error')
        return render_template('pick_playername.html',
                               current_name=player_name,
                               max_playername_length=MAX_PLAYERNAME_LENGTH)

    session['player_name'] = player_name
    flash('Successful username created.', 'success')
    return redirect(url_for('play_game'))

@app.route('/new_player')
def new_player():
    session.pop('player_name')
    return redirect(url_for('enter_playername'))

@app.route('/play')
@requires_playername
def play_game():
    session['round'] = 0
    session['score'] = 0
    return render_template('play_game.html', player_name=session['player_name'])

@app.route('/play/player_turn')
@requires_playername
def player_turn():
    session['round'] += 1
    return render_template('player_turn.html',
                           round_number=session['round'],
                           max_rounds=MAX_ROUNDS_PER_GAME)

@app.route('/play/computer_turn', methods=['POST'])
@requires_playername
def computer_turn():
    player_move = request.form['move']
    computer_move = get_computer_move()
    winning_move = determine_winning_move(player_move, computer_move)
    winning_method = get_winning_method(player_move, computer_move)

    if winning_move:
        if player_move == winning_move:
            result = 'player'
            session['score'] += 1
        else:
            result = 'computer'
    else:
        result = 'tie'
        session['round'] -= 1

    session['player_move'] = player_move
    session['computer_move'] = computer_move
    session['winning_move'] = winning_move
    session['winning_method'] = winning_method
    session['result'] = result

    return redirect(url_for('display_outcome'))

@app.route('/play/outcome')
@requires_playername
def display_outcome():
    player_move = session.get('player_move')
    computer_move = session.get('computer_move')
    winning_move = session.get('winning_move')
    winning_method = session.get('winning_method')
    result = session.get('result')

    final_round = session['round'] >= MAX_ROUNDS_PER_GAME
    included_on_leaderboard = False

    if final_round:
        leaderboard = g.leaderboard_storage.get_leaderboard()

        if src.rpsls_online.utils.include_score_in_leaderboard(session['score'], leaderboard):
            g.leaderboard_storage.update_leaderboard(session['player_name'], session['score'])
            included_on_leaderboard = True

    return render_template(
        'outcome.html',
        player_move=player_move,
        computer_move=computer_move,
        winning_move=winning_move,
        result=result,
        winning_method=winning_method,
        final_round=final_round,
        score=session['score'],
        max_rounds=MAX_ROUNDS_PER_GAME,
        included=included_on_leaderboard)

if __name__ == '__main__':
    if os.environ.get('FLASK_ENV') == 'production':
        app.run(debug=False)
    else:
        app.run(debug=True, port=5003)

# TODO: Refresh page leads to errors