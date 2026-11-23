# Connect 4 - Minimax with Alpha-Beta (AI Assignment 2)

Board is 7 columns x 6 rows. Human = X / red, AI = O / yellow.
The game continues until the board is full, the winner has more connected-fours.

## Run
    python3 gui.py          (tkinter window, needs python3-tk on Linux)
    python3 console.py      (Member 2 has to finish it)
    python3 benchmark.py    (K = 1..5, writes benchmark_results.csv)

## Files
| File | Status | What it does |
|------|--------|--------------|
| board.py | DONE | board, drop piece, valid moves (center first), count fours, board text |
| minimax.py | DONE | minimax + alpha-beta, K-depth cutoff, tree printing with alpha/beta, pruned cols, leaf heuristic values and boards, nodes + time |
| gui.py | DONE | GUI with K spinbox, click to play, scores, tree panel, nodes/time. Full tree is also printed to console and saved in tree_log.txt |
| benchmark.py | DONE | AI vs random player, nodes and time per K, with and without pruning |
| heuristic.py | MEMBER 2 | placeholder only (score difference). Real heuristic must be designed here |
| console.py | MEMBER 2 | only a skeleton, console game loop is missing |
| Report | MEMBER 2 | not started |

## Member 2 checklist
1. heuristic.py - design the real heuristic (bonus for best 3). Use current scores, open 3s and 2s, center control, candidate cells. Keep it fast because it runs on every leaf.
2. console.py - ask for K, play the game, print board and tree every turn.
3. Run benchmark.py again after the heuristic is done and use benchmark_results.csv in the report.
4. Report: sample runs with their trees, time and nodes table for different K (pruning vs plain), data structures (list of lists board, list of strings for tree), algorithm explanation, heuristic explanation, assumptions, extra work (GUI + tree panel).
5. Before submitting add comments to the code, the assignment asks for well commented code.

## Assumptions
- A line of 5 or more discs counts as more than one four (every window of 4 is counted).
- Human always plays first.
- Full board value is (AI fours - human fours) * 1000, so real results beat heuristic values.
