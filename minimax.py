import time
from board import valid_moves, drop_piece, count_fours, board_to_text, HUMAN, AI
from heuristic import evaluate

# used for alpha and beta at the start
INF = float("inf")


# returns (value, best column)
def minimax(board, depth, alpha, beta, maximizing, stats, lines, indent, move, prune, show_boards):
    stats["nodes"] += 1
    pad = "    " * indent
    label = "root" if move is None else "col " + str(move)
    moves = valid_moves(board)

    # stop when depth ends or the board is full
    if depth == 0 or len(moves) == 0:
        if len(moves) == 0:
            # board is full so use the real score
            value = (count_fours(board, AI) - count_fours(board, HUMAN)) * 1000
            kind = "FULL"
        else:
            value = evaluate(board)
            kind = "LEAF"
        if lines is not None:
            lines.append(pad + label + " " + kind + " h=" + str(value))
            if show_boards:
                for row in board_to_text(board):
                    lines.append(pad + "    " + row)
        return value, None

    # save the line place so i can write the value after the children
    spot = None
    if lines is not None:
        spot = len(lines)
        lines.append("")

    best_col = None
    # ai turn, take the biggest value
    if maximizing:
        kind = "MAX"
        best = -INF
        for i in range(len(moves)):
            col = moves[i]
            child = drop_piece(board, col, AI)
            val, _ = minimax(child, depth - 1, alpha, beta, False, stats, lines, indent + 1, col, prune, show_boards)
            # keep the best move so far
            if val > best:
                best = val
                best_col = col
            alpha = max(alpha, best)
            # cut off the rest of the columns
            if prune and alpha >= beta:
                rest = moves[i + 1:]
                if rest and lines is not None:
                    lines.append(pad + "    pruned cols " + str(rest))
                break
    # human turn, take the smallest value
    else:
        kind = "MIN"
        best = INF
        for i in range(len(moves)):
            col = moves[i]
            child = drop_piece(board, col, HUMAN)
            val, _ = minimax(child, depth - 1, alpha, beta, True, stats, lines, indent + 1, col, prune, show_boards)
            if val < best:
                best = val
                best_col = col
            beta = min(beta, best)
            if prune and alpha >= beta:
                rest = moves[i + 1:]
                if rest and lines is not None:
                    lines.append(pad + "    pruned cols " + str(rest))
                break

    if lines is not None:
        lines[spot] = pad + label + " " + kind + " value=" + str(best) + " alpha=" + str(alpha) + " beta=" + str(beta)
    return best, best_col


# called from the gui and the benchmark
def choose_move(board, k, prune=True, show_boards=True, build_tree=True):
    stats = {"nodes": 0}
    lines = [] if build_tree else None
    start = time.time()
    value, col = minimax(board, k, -INF, INF, True, stats, lines, 0, None, prune, show_boards)
    elapsed = time.time() - start
    return {"col": col, "value": value, "nodes": stats["nodes"], "time": elapsed, "tree": lines}
