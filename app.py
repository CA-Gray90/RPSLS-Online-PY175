from flask import (
    Flask,
    g,
    render_template,
    redirect,
    request,
    session,
    url_for
    )

app = Flask(__name__)
app.secret_key = '!i_love_rpsls_online!'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/rules')
def display_rules():
    return render_template('rules.html')

@app.route('/sign_in')
def sign_in():
    return render_template('sign_in.html')

@app.route('/leaderboard')
def display_leaderboard():
    # Retrieve leadboard file
    # display leaderboard > pass it to template
    return render_template('leaderboard.html')

@app.route('/play')
def play_game():
    return render_template('play_game.html')

@app.route('/play/player_turn')
def player_turn():
    return render_template('player_turn.html')

@app.route('/play/computer_turn', methods=['POST'])
def computer_turn():
    # Get the request object
    # retrive the move the player made
    # run the logic to determine computers move
    # run the logic to determine winner of the round
    # place moves and outcome into g object?
        # g.players_move = 'rock'
        # g.computers_move = 
        # g.winner = computer/player
    # redirect to display outcome page
    session['player_move'] = request.form['move']
    print(f'Players move captured: {session['player_move']}')
    return redirect(url_for('display_outcome'))

@app.route('/play/outcome')
def display_outcome():
    print(f'players move direct from session: {session.get('player_move')}')
    player_move = session.pop('player_move')
    print(f'Players move after redirect: {player_move}')
    # retrieve outcome and moves from g object?
    # render template with outcome, moves etc. All info needed to display what happened in the round
    # play again or quit
    return render_template('outcome.html', player_move=player_move)

if __name__ == '__main__':
    app.run(debug=True, port=5003)