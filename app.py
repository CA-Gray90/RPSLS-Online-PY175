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

from rpsls_online.game_logic import (
    get_computer_move,
    get_winning_method,
    determine_winning_move)

import os, secrets, rpsls_online.utils, yaml

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

MAX_PLAYERNAME_LENGTH = 10
MAX_ROUNDS_PER_GAME = 5

@app.before_request
def get_data_path():
    root = os.path.abspath(os.path.dirname(__file__))
    g.data_dir = os.path.join(root, 'rpsls_online', 'data')
    g.leaderboard_filepath = os.path.join(g.data_dir, 'leaderboard.yaml')

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
    leaderboard = rpsls_online.utils.get_leaderboard(g.leaderboard_filepath)
    return render_template('leaderboard.html', leaderboard=leaderboard)

@app.route('/enter_playername')
def enter_playername():
    return render_template('pick_playername.html',
                           max_playername_length=MAX_PLAYERNAME_LENGTH)

@app.route('/enter_playername/validate', methods=['POST'])
def validate_playername():
    player_name = request.form['player_name'].strip()

    if not rpsls_online.utils.valid_player_name(player_name):
        flash('Not a valid username. Use only numbers and letters. Try again.',
              'error')
        return render_template('pick_playername.html',
                               current_name=player_name,
                               max_playername_length=MAX_PLAYERNAME_LENGTH)

    leaderboard = dict(rpsls_online.utils.get_leaderboard(g.leaderboard_filepath))

    if player_name in leaderboard.keys():
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
def play_game():
    session['round'] = 0
    session['score'] = 0
    return render_template('play_game.html', player_name=session['player_name'])

@app.route('/play/player_turn')
def player_turn():
    session['round'] += 1
    return render_template('player_turn.html',
                           round_number=session['round'],
                           max_rounds=MAX_ROUNDS_PER_GAME)

@app.route('/play/computer_turn', methods=['POST'])
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
def display_outcome():
    player_move = session.pop('player_move')
    computer_move = session.pop('computer_move')
    winning_move = session.pop('winning_move')
    winning_method = session.pop('winning_method')
    result = session.pop('result')

    final_round = session['round'] >= MAX_ROUNDS_PER_GAME
    included_on_leaderboard = False

    if final_round:
        leaderboard = rpsls_online.utils.get_leaderboard(g.leaderboard_filepath)

        if rpsls_online.utils.include_score_in_leaderboard(session['score'], leaderboard):
            leaderboard = rpsls_online.utils.update_leaderboard(session['player_name'], session['score'], leaderboard)

            with open(g.data_dir + '/leaderboard.yaml', 'w') as file:
                yaml.safe_dump(dict(leaderboard), file)
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