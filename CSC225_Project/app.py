from flask import Flask, render_template, request, jsonify
from ai import get_winning_cells
import ai
import os

app = Flask(__name__, template_folder='d:\\CSC225_Project\\templates')
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'dev')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/move', methods=['POST'])
def move():
    data = request.get_json()
    board = data['board']
    player = data['player']

    win = ai.check_win(board, 'X') or ai.check_win(board, 'O')
    tie = all(cell != '' for row in board for cell in row) and not win

    # Determine the winner correctly
    if ai.check_win(board, 'X'):
        winner = 'X'
    elif ai.check_win(board, 'O'):
        winner = 'O'
    else:
        winner = None

    ai_move = None
    if not win and not tie and player == 'X':
        ai_move = ai.get_ai_move(board, 'O')
        if ai_move:
            board[ai_move[0]][ai_move[1]] = 'O'
            # Re-check for win/tie after AI move
            if ai.check_win(board, 'O'):
                win = True
                winner = 'O'
            tie = all(cell != '' for row in board for cell in row) and not win

    # Get the winning cells for the winner, if any
    if winner:
        winning_cells = get_winning_cells(board, winner)
    else:
        winning_cells = []

    response = jsonify({
        'ai_move': ai_move,
        'win': win,
        'tie': tie,
        'board': board,
        'winner': winner,
        'winning_cells': winning_cells
    })

    # Check if the game is over on the server side and send the status
    if win or tie:
        response.json['game_over'] = True
        response.json['status'] = f"{winner} wins!" if winner else "It's a tie!"

    return response

@app.route('/restart', methods=['POST'])
def restart():
    board = [['' for _ in range(3)] for _ in range(3)]
    return jsonify({'board': board})

if __name__ == '__main__':
    app.run(debug=True)