# Connect 4 - Minimax with Alpha-Beta Pruning (AI Assignment 2)

Human vs computer Connect 4 on a 7 columns x 6 rows board.
Human = X / red (plays first), AI = O / yellow.
The game continues until the board is full; the player with more connected-fours wins.

## Run
    python3 console.py      # console game (asks for K, prints board + minimax tree every turn)
    python3 gui.py          # tkinter GUI (needs python3-tk on Linux), K spin box + tree panel
    python3 benchmark.py    # K = 1..5, alpha-beta vs plain minimax, writes benchmark_results.csv

Only the Python 3 standard library is used.

## Files
| File | What it does |
|------|--------------|
| board.py | board (list of lists), drop piece, valid moves (centre first), windows of 4, count fours, board as text |
| minimax.py | minimax + alpha-beta, K-depth cut-off, tree printing (alpha/beta, pruned columns, leaf heuristic values and boards), node count and time |
| heuristic.py | heuristic evaluation of a board (see below) |
| console.py | console version of the game |
| gui.py | GUI (bonus): click to play, scores, K spin box, tree panel, nodes/time; full trees saved to tree_log.txt |
| benchmark.py | AI vs random player, nodes and time for each K, with and without pruning |
| report.tex / report.pdf | the report |

## Algorithm
- AI = MAX, human = MIN. The search stops at depth K and evaluates the leaf with the heuristic.
- A full board is scored as (AI fours - human fours) * 1000, so real results always beat heuristic values.
- Alpha-beta cuts the remaining columns when alpha >= beta; pruned columns are printed in the tree.
- Columns are tried centre-first to get more cut-offs.

## Heuristic (heuristic.py)
One pass over the 69 windows of 4 cells. A window with discs of only one player is a possible future four for that player.

| Feature | AI | Human |
|---------|----|-------|
| completed four | +100 | -100 |
| 3 discs + 1 empty | +10 | -12 |
| 2 discs + 2 empty | +3 | -4 |
| disc in centre column | +4 | -4 |

Windows containing both players' discs are ignored. Human threats weigh slightly more, which makes the AI a bit defensive.

## Tree format
    col 3 MIN value=-25 alpha=-inf beta=-25    internal node (value, alpha, beta when finished)
    col 4 LEAF h=-25                           leaf: heuristic value (+ board if enabled)
    col 2 FULL h=1000                          full board: real score * 1000
    pruned cols [2, 4, 1]                      columns skipped by alpha-beta

## Assumptions
- Human always plays first.
- A line of 5 or more discs counts as more than one four (every window of 4 is counted).
- The game ends only when the board is full.
- Equal number of fours = draw.