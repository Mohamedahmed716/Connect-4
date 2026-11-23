from board import count_fours, HUMAN, AI


def evaluate(board):
    # TODO Member 2: replace this placeholder with the real heuristic.
    # Higher number = AI is closer to winning, lower = human is closer.
    # Ideas to use: current scores, open 3s / 2s for each player (windows with
    # no opponent disc), center column control, playable candidate cells.
    # Weights should be explained in the report.
    return count_fours(board, AI) - count_fours(board, HUMAN)
