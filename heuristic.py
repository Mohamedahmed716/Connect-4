from board import get_windows, ROWS, COLS, HUMAN, AI

# Weights (explained in the report)
W_FOUR = 100       # a completed four (real score)
W_THREE = 10       # window: 3 AI discs + 1 empty (open three)
W_TWO = 3          # window: 2 AI discs + 2 empty (open two)
W_THREE_OPP = 12   # human open three (slightly higher -> defensive)
W_TWO_OPP = 4      # human open two
W_CENTER = 4       # each disc in the centre column


def evaluate(board):
    score = 0
    # one pass over all 69 windows of 4 cells
    for w in get_windows(board):
        ai = w.count(AI)
        hu = w.count(HUMAN)
        if hu == 0:                    # window can still only be used by the AI
            if ai == 4:
                score += W_FOUR
            elif ai == 3:
                score += W_THREE
            elif ai == 2:
                score += W_TWO
        elif ai == 0:                  # window can still only be used by the human
            if hu == 4:
                score -= W_FOUR
            elif hu == 3:
                score -= W_THREE_OPP
            elif hu == 2:
                score -= W_TWO_OPP
        # mixed windows (both players present) can never become a four -> ignored
    # centre column belongs to the most windows, so discs there are worth more
    mid = COLS // 2
    for r in range(ROWS):
        if board[r][mid] == AI:
            score += W_CENTER
        elif board[r][mid] == HUMAN:
            score -= W_CENTER
    return score