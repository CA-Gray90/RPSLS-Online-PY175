from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/rules')
def display_rules():
    return render_template('rules.html')

@app.route('/sign_in')
def sign_in():
    return render_template('sign_in.html')

@app.route('/play')
def play_game():
    return render_template('play_game.html')

@app.route('/leaderboard')
def display_leaderboard():
    # Retrieve leadboard file
    # display leaderboard > pass it to template
    return render_template('leaderboard.html')

if __name__ == '__main__':
    app.run(debug=True, port=5003)