import random

def get_ai_move(board, player):
    opponent = 'X' if player == 'O' else 'O'

    # Try to win
    for i in range(3):
        for j in range(3):
            if board[i][j] == '':
                board[i][j] = player
                if check_win(board, player):
                    board[i][j] = ''
                    return (i, j)
                board[i][j] = ''

    # Try to block opponent
    for i in range(3):
        for j in range(3):
            if board[i][j] == '':
                board[i][j] = opponent
                if check_win(board, opponent):
                    board[i][j] = ''
                    return (i, j)
                board[i][j] = ''

    # Pick random move
    empty_cells = [(i, j) for i in range(3) for j in range(3) if board[i][j] == '']
    return random.choice(empty_cells) if empty_cells else None

def check_win(board, player):
    # Check rows and columns
    for i in range(3):
        if all(board[i][j] == player for j in range(3)):
            return True
        if all(board[j][i] == player for j in range(3)):
            return True
    # Check diagonals
    if all(board[d][d] == player for d in range(3)):
        return True
    if all(board[d][2 - d] == player for d in range(3)):
        return True
    return False

def get_winning_cells(board, player):
    # Rows
    for i in range(3):
        if all(board[i][j] == player for j in range(3)):
            return [[i, j] for j in range(3)]
    # Columns
    for j in range(3):
        if all(board[i][j] == player for i in range(3)):
            return [[i, j] for i in range(3)]
    # Diagonals
    if all(board[d][d] == player for d in range(3)):
        return [[d, d] for d in range(3)]
    if all(board[d][2-d] == player for d in range(3)):
        return [[d, 2-d] for d in range(3)]
    return []