# board size
ROWS = 6
COLS = 7
# numbers used to mark the cells
EMPTY = 0
HUMAN = 1
AI = 2

# try middle columns first, they are usually better
ORDER = sorted(range(COLS), key=lambda c: abs(c - COLS // 2))


def new_board():
    return [[EMPTY] * COLS for _ in range(ROWS)]


def copy_board(board):
    return [row[:] for row in board]


# a column is ok if its top cell is empty
def valid_moves(board):
    return [c for c in ORDER if board[0][c] == EMPTY]


def is_full(board):
    return len(valid_moves(board)) == 0


# copy the board so the old one doesnt change
def drop_piece(board, col, player):
    new = copy_board(board)
    # start from the bottom row and go up
    for r in range(ROWS - 1, -1, -1):
        if new[r][col] == EMPTY:
            new[r][col] = player
            return new
    return None


# all groups of 4 cells in a line
def get_windows(board):
    windows = []
    for r in range(ROWS):
        for c in range(COLS):
            # horizontal
            if c + 3 < COLS:
                windows.append([board[r][c + i] for i in range(4)])
            # vertical
            if r + 3 < ROWS:
                windows.append([board[r + i][c] for i in range(4)])
            # diagonal down right
            if r + 3 < ROWS and c + 3 < COLS:
                windows.append([board[r + i][c + i] for i in range(4)])
            # diagonal down left
            if r + 3 < ROWS and c - 3 >= 0:
                windows.append([board[r + i][c - i] for i in range(4)])
    return windows


# a window full of the same player is one four
def count_fours(board, player):
    total = 0
    for w in get_windows(board):
        if w.count(player) == 4:
            total += 1
    return total


def board_to_text(board):
    symbols = {EMPTY: ".", HUMAN: "X", AI: "O"}
    rows = [" ".join(symbols[x] for x in row) for row in board]
    rows.append(" ".join(str(c) for c in range(COLS)))
    return rows
