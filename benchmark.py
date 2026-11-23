import random
import csv
from board import *
from minimax import choose_move


# human is a random player here
def play_game(k, prune, seed):
    random.seed(seed)
    board = new_board()
    total_nodes = 0
    total_time = 0.0
    ai_moves = 0
    while not is_full(board):
        col = random.choice(valid_moves(board))
        board = drop_piece(board, col, HUMAN)
        if is_full(board):
            break
        result = choose_move(board, k, prune, False, False)
        board = drop_piece(board, result["col"], AI)
        total_nodes += result["nodes"]
        total_time += result["time"]
        ai_moves += 1
    return total_nodes, total_time, ai_moves


# compare alpha beta with plain minimax for each K
def main():
    rows = []
    print("K  pruning  total_nodes  avg_nodes/move  total_time(s)  avg_time/move(s)")
    for k in range(1, 6):
        for prune in (True, False):
            # plain minimax at k=5 takes too long
            if not prune and k > 4:
                continue
            nodes, t, moves = play_game(k, prune, 1)
            row = [k, "alpha-beta" if prune else "plain", nodes, round(nodes / moves, 1), round(t, 3), round(t / moves, 4)]
            rows.append(row)
            print(*row, sep="   ")
    with open("benchmark_results.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["K", "algorithm", "total_nodes", "avg_nodes_per_move", "total_time_s", "avg_time_per_move_s"])
        w.writerows(rows)


if __name__ == "__main__":
    main()
