import tkinter as tk
from tkinter import messagebox
from board import *
from minimax import choose_move

# size of one cell in pixels
CELL = 80
# the text box gets slow with a huge tree
MAX_TREE_LINES = 3000


class Connect4App:
    def __init__(self, root):
        self.root = root
        root.title("Connect 4 - Minimax AI")

        top = tk.Frame(root)
        top.pack(side=tk.TOP, fill=tk.X, padx=8, pady=6)
        tk.Label(top, text="K (depth):").pack(side=tk.LEFT)
        self.k_var = tk.IntVar(value=3)
        tk.Spinbox(top, from_=1, to=8, width=3, textvariable=self.k_var).pack(side=tk.LEFT, padx=4)
        self.boards_var = tk.BooleanVar(value=False)
        tk.Checkbutton(top, text="show boards in tree", variable=self.boards_var).pack(side=tk.LEFT, padx=8)
        tk.Button(top, text="New Game", command=self.new_game).pack(side=tk.LEFT, padx=8)

        self.score_label = tk.Label(top, text="", font=("Arial", 11, "bold"))
        self.score_label.pack(side=tk.RIGHT)

        middle = tk.Frame(root)
        middle.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=8)

        self.canvas = tk.Canvas(middle, width=COLS * CELL, height=ROWS * CELL, bg="#1f4fd8", highlightthickness=0)
        self.canvas.pack(side=tk.LEFT)
        self.canvas.bind("<Button-1>", self.on_click)

        right = tk.Frame(middle)
        right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(8, 0))
        tk.Label(right, text="Minimax tree of last AI move").pack(anchor="w")
        self.tree_text = tk.Text(right, width=55, height=ROWS * 5, font=("Courier", 9), wrap="none")
        scroll_y = tk.Scrollbar(right, command=self.tree_text.yview)
        scroll_x = tk.Scrollbar(right, orient=tk.HORIZONTAL, command=self.tree_text.xview)
        self.tree_text.config(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.info_label = tk.Label(root, text="", anchor="w")
        self.info_label.pack(side=tk.BOTTOM, fill=tk.X, padx=8, pady=6)

        self.new_game()

    # reset everything
    def new_game(self):
        self.board = new_board()
        self.k = int(self.k_var.get())
        self.busy = False
        self.over = False
        self.move_number = 0
        self.tree_text.delete("1.0", tk.END)
        self.info_label.config(text="Your turn (red). Click a column.")
        self.draw()

    # draw all the circles again
    def draw(self):
        self.canvas.delete("all")
        colors = {EMPTY: "#d9d9d9", HUMAN: "#e02020", AI: "#f5d90a"}
        for r in range(ROWS):
            for c in range(COLS):
                x1 = c * CELL + 8
                y1 = r * CELL + 8
                self.canvas.create_oval(x1, y1, x1 + CELL - 16, y1 + CELL - 16,
                                        fill=colors[self.board[r][c]], outline="#12307f", width=2)
        h = count_fours(self.board, HUMAN)
        a = count_fours(self.board, AI)
        self.score_label.config(text="You: " + str(h) + "    AI: " + str(a))

    # x position tells which column was clicked
    def on_click(self, event):
        if self.busy or self.over:
            return
        col = event.x // CELL
        if col not in valid_moves(self.board):
            return
        self.board = drop_piece(self.board, col, HUMAN)
        self.draw()
        if is_full(self.board):
            self.finish()
            return
        self.busy = True
        self.info_label.config(text="AI is thinking...")
        # small delay so the board updates before the ai thinks
        self.root.after(50, self.ai_turn)

    # run minimax and show the tree
    def ai_turn(self):
        self.move_number += 1
        result = choose_move(self.board, self.k, True, self.boards_var.get(), True)
        tree = result["tree"]

        header = "===== AI move " + str(self.move_number) + " (K=" + str(self.k) + ") ====="
        print(header)
        print("\n".join(tree))
        print("chosen col:", result["col"], "value:", result["value"])
        # save the full tree in a file too
        with open("tree_log.txt", "a") as f:
            f.write(header + "\n" + "\n".join(tree) + "\n\n")

        self.tree_text.delete("1.0", tk.END)
        shown = tree[:MAX_TREE_LINES]
        self.tree_text.insert(tk.END, "\n".join(shown))
        if len(tree) > MAX_TREE_LINES:
            self.tree_text.insert(tk.END, "\n... " + str(len(tree) - MAX_TREE_LINES) + " more lines (see tree_log.txt)")

        self.board = drop_piece(self.board, result["col"], AI)
        self.draw()
        self.info_label.config(text="AI played column " + str(result["col"]) +
                               " | nodes: " + str(result["nodes"]) +
                               " | time: " + str(round(result["time"], 3)) + "s | value: " + str(result["value"]))
        self.busy = False
        if is_full(self.board):
            self.finish()

    # the one with more fours wins
    def finish(self):
        self.over = True
        h = count_fours(self.board, HUMAN)
        a = count_fours(self.board, AI)
        if h > a:
            msg = "You win!"
        elif a > h:
            msg = "AI wins!"
        else:
            msg = "It's a draw!"
        self.info_label.config(text="Board full. " + msg)
        messagebox.showinfo("Game over", msg + "\nYou: " + str(h) + "  AI: " + str(a))


def main():
    root = tk.Tk()
    Connect4App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
