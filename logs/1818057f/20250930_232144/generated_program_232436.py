```python
from typing import List

def fill_h_pattern(grid: List[List[int]], bar_row: int, bar_start_col: int) -> None:
    """
    Fills the positions of an H pattern with 8, assuming the input conditions are met.
    This handles the rule for identifying and coloring H-shaped structures made of 4's.
    """
    center_col = bar_start_col + 1
    grid[bar_row - 1][center_col] = 8
    grid[bar_row][bar_start_col] = 8
    grid[bar_row][center_col] = 8
    grid[bar_row][bar_start_col + 2] = 8
    grid[bar_row + 1][center_col] = 8

def program(g: List[List[int]]) -> List[List[int]]:
    """
    Main program: Copies the input grid and applies the H-pattern filling rule
    to transform certain 4's into 8's based on the observed puzzle mechanics.
    """
    if not g:
        return []
    h = len(g)
    w = len(g[0])
    output = [row[:] for row in g]
    for r in range(1, h - 1):
        for c in range(w - 2):
            if (g[r][c] == 4 and
                g[r][c + 1] == 4 and
                g[r][c + 2] == 4 and
                g[r - 1][c + 1] == 4 and
                g[r + 1][c + 1] == 4):
                fill_h_pattern(output, r, c)
    return output
```