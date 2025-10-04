```python
from typing import List

def copy_grid(g: List[List[int]]) -> List[List[int]]:
    # Rule: Create a deep copy of the input grid to avoid mutating the original
    return [row[:] for row in g]

def find_seed_row(g: List[List[int]]) -> int:
    # Observation: The seed row is the first row containing the fill color 2 (maroon), typically in the main area
    h = len(g)
    for r in range(h):
        if 2 in g[r]:
            return r
    return -1  # No seed found

def detect_clue_cols(g: List[List[int]]) -> List[int]:
    # Observation: Clue columns are detected in row 1 (top pattern row), at approximate section starts every 6 columns,
    # where the cell is a non-background, non-border, non-empty color (clues for branches)
    w = len(g[0]) if g else 0
    clue_cols = []
    for c in range(1, w - 1, 6):  # Step of 6 to hit section starts like 1,7,13,19,...
        if g[1][c] not in (0, 6, 8):
            clue_cols.append(c)
    return clue_cols

def fill_horizontal(g: List[List[int]], r: int, start_c: int, end_c: int) -> None:
    # Rule: Fill horizontal line at row r from start_c to end_c with 2 (maroon) only in background (0) or empty (8) cells
    for c in range(start_c, end_c + 1):
        if g[r][c] in (0, 8):
            g[r][c] = 2

def fill_vertical(g: List[List[int]], c: int, start_r: int, end_r: int) -> None:
    # Rule: Fill vertical line at column c from start_r to end_r with 2 (maroon) only in background (0) or empty (8) cells
    for r in range(start_r, end_r + 1):
        if g[r][c] in (0, 8):
            g[r][c] = 2

def program(g: List[List[int]]) -> List[List[int]]:
    # Compose rules: Copy grid, find seed row for horizontal connection, detect clue columns for vertical branches,
    # fill horizontal at seed row to connect across, fill vertical branches full height to link top to bottom
    new_g = copy_grid(g)
    seed_r = find_seed_row(new_g)
    h, w = len(new_g), len(new_g[0]) if new_g else 0
    if seed_r != -1:
        # Fill horizontal connection at seed row across all columns
        fill_horizontal(new_g, seed_r, 0, w - 1)
        # Detect clue columns and fill vertical branches full height
        clue_cols = detect_clue_cols(new_g)
        for c in clue_cols:
            fill_vertical(new_g, c, 0, h - 1)
    return new_g
```