from board import *
from minimax import choose_move


# ask until the user types an integer in [low, high]
def ask_int(text, low, high):
    while True:
        s = input(text).strip()
        if s.isdigit() and low <= int(s) <= high:
            return int(s)
        print("Please enter a number between", low, "and", high)


def print_board(board):
    print("\n".join(board_to_text(board)))
    print("You (X):", count_fours(board, HUMAN), "  AI (O):", count_fours(board, AI))


def main():
    print("Connect 4 - you are X (first), AI is O")
    k = ask_int("Enter K (search depth, 1-8): ", 1, 8)
    show = input("Show boards inside the tree? (y/n): ").strip().lower() == "y"
    board = new_board()
    print_board(board)
    move_no = 0
    while not is_full(board):
        # human turn (re-ask if the column is full)
        free = valid_moves(board)
        while True:
            col = ask_int("Your column (0-" + str(COLS - 1) + "): ", 0, COLS - 1)
            if col in free:
                break
            print("Column", col, "is full.")
        board = drop_piece(board, col, HUMAN)
        print_board(board)
        if is_full(board):
            break
        # AI turn: run minimax + alpha-beta and print the whole tree
        move_no += 1
        result = choose_move(board, k, True, show, True)
        print("\n===== Minimax tree, AI move", move_no, "(K=" + str(k) + ") =====")
        print("\n".join(result["tree"]))
        print("chosen col:", result["col"], "value:", result["value"],
              "nodes:", result["nodes"], "time: %.3fs" % result["time"])
        board = drop_piece(board, result["col"], AI)
        print_board(board)
    h, a = count_fours(board, HUMAN), count_fours(board, AI)
    print("\nBoard full. Final score -> You:", h, " AI:", a)
    print("You win!" if h > a else "AI wins!" if a > h else "Draw!")


if __name__ == "__main__":
    main()