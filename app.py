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

import game_logic, os, utils, yaml

app = Flask(__name__)
app.secret_key = '!i_love_rpsls_online!'

MAX_PLAYERNAME_LENGTH = 10
MAX_ROUNDS_PER_GAME = 5

@app.before_request
def get_data_path():
    root = os.path.abspath(os.path.dirname(__file__))
    g.data_dir = os.path.join(root, 'rpsls_online', 'data')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/rules')
def display_rules():
    with open(g.data_dir + '/rules.yaml', 'r') as file:
        rules = yaml.safe_load(file)

    opening_lines = rules['opening_lines']
    game_actions = rules['game_actions']
    return render_template('rules.html',
                           opening_lines=opening_lines,
                           game_actions=game_actions)

@app.route('/leaderboard')
def display_leaderboard():
    with open(g.data_dir + '/leaderboard.yaml', 'r') as file:
        leaderboard = [(name, score) for name, score in yaml.safe_load(file).items()]
        leaderboard.sort(key=lambda tup: tup[1], reverse=True)
    return render_template('leaderboard.html', leaderboard=leaderboard)

@app.route('/enter_playername')
def enter_playername():
    return render_template('pick_playername.html',
                           max_playername_length=MAX_PLAYERNAME_LENGTH)

@app.route('/enter_playername/validate', methods=['POST'])
def validate_playername():
    player_name = request.form['player_name'].strip()
    if not utils.valid_player_name(player_name, MAX_PLAYERNAME_LENGTH):
        flash('Not a valid username. Try again.')
        return render_template('pick_playername.html', current_name=player_name)
        
    with open(g.data_dir + '/leaderboard.yaml', 'r') as file:
        leaderboard = yaml.safe_load(file)
    if player_name in leaderboard.keys():
        flash('Please choose another username, current one in leaderboard.')
        return render_template('pick_playername.html', current_name=player_name)

    session['player_name'] = player_name
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
    computer_move = game_logic.get_computer_move()
    winning_move = game_logic.determine_winning_move(player_move, computer_move)

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
    session['winning_method'] = game_logic.get_winning_method(player_move, 
                                                              computer_move)
    session['result'] = result

    return redirect(url_for('display_outcome'))

@app.route('/play/outcome')
def display_outcome():
    final_round = session['round'] >= 5
    player_move = session.pop('player_move')
    computer_move = session.pop('computer_move')
    winning_move = session.pop('winning_move')
    winning_method = session.pop('winning_method')
    result = session.pop('result')
    included_on_leaderboard = False

    if final_round:
        with open(g.data_dir + '/leaderboard.yaml', 'r') as file:
                leaderboard = [(name, score) for name, score in yaml.safe_load(file).items()]
                leaderboard.sort(key=lambda tup: tup[1], reverse=True)

        if utils.include_score_in_leaderboard(session['score'], leaderboard):
            leaderboard = utils.update_leaderboard(session['player_name'], session['score'], leaderboard)

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
    app.run(debug=True, port=5003)

# TODO: Separate functionality, DRY the code?
# TODO: Clean up UI a bit with basic CSS