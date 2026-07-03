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

PLAYER_NAME_LENGTH = 8

@app.before_request
def get_data_path():
    root = os.path.abspath(os.path.dirname(__file__))
    g.data_dir = os.path.join(root, 'rpsls_online', 'data')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/rules')
def display_rules():
    return render_template('rules.html')

@app.route('/leaderboard')
def display_leaderboard():
    # Retrieve leadboard file
    # display leaderboard > pass it to template
    return render_template('leaderboard.html')

@app.route('/enter_playername')
def enter_playername():
    return render_template('pick_playername.html')

@app.route('/enter_playername/validate', methods=['POST'])
def validate_playername():
    player_name = request.form['player_name'].strip()
    # Implement logic to validate username:
        # not longer than 8 chars long
        # not in the leaderboard, saved names
            # retrieve and open the file
            # check against the names in the file
    if not utils.valid_player_name(player_name, PLAYER_NAME_LENGTH):
        flash('Not a valid username. Try again.')
        return render_template('pick_playername.html', current_name=player_name)
        
    with open(g.data_dir + '/leaderboard.yaml', 'r') as file:
        leaderboard = yaml.safe_load(file)
    if player_name in leaderboard.keys():
        flash('Please choose another username, current one in leaderboard.')
        return render_template('pick_playername.html', current_name=player_name)

    session['player_name'] = player_name
    return render_template('play_game.html', player_name=player_name)
    

@app.route('/new_player')
def new_player():
    session.pop('player_name')
    return redirect(url_for('enter_playername'))

@app.route('/play')
def play_game():
    return render_template('play_game.html')

@app.route('/play/player_turn')
def player_turn():
    return render_template('player_turn.html')

@app.route('/play/computer_turn', methods=['POST'])
def computer_turn():
    player_move = request.form['move']
    computer_move = game_logic.get_computer_move()
    winning_move = game_logic.determine_winning_move(player_move, computer_move)
    if winning_move:
        if player_move == winning_move:
            result = 'player'
        else:
            result = 'computer'
    else:
        result = 'tie'

    session['player_move'] = player_move
    session['computer_move'] = computer_move
    session['winning_move'] = winning_move
    session['winning_method'] = game_logic.get_winning_method(player_move, computer_move)
    session['result'] = result

    return redirect(url_for('display_outcome'))

@app.route('/play/outcome')
def display_outcome():
    # retrieve outcome and moves from g object?
    # render template with outcome, moves etc. All info needed to display what happened in the round
    # play again or quit
    player_move = session.pop('player_move')
    computer_move = session.pop('computer_move')
    winning_move = session.pop('winning_move')
    winning_method = session.pop('winning_method')
    result = session.pop('result')

    return render_template(
        'outcome.html',
        player_move=player_move,
        computer_move=computer_move,
        winning_move=winning_move,
        result=result,
        winning_method=winning_method)

if __name__ == '__main__':
    app.run(debug=True, port=5003)