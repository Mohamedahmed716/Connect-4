from board import *
from minimax import choose_move


def main():
    # TODO Member 2: write the console version of the game.
    # 1) ask the user for K before the game starts
    # 2) loop: human types a column (validate it), AI answers using
    #    choose_move(board, k) which returns a dict with col, value, nodes, time, tree
    # 3) print the board with board_to_text(board) after every move
    # 4) print the tree: print("\n".join(result["tree"]))
    # 5) stop when is_full(board) and print the winner using count_fours
    print("console mode is not implemented yet")


if __name__ == "__main__":
    main()
