```python
from typing import List

def has_plus_pattern(grid: List[List[int]], r: int, c: int) -> bool:
    """
    Checks if there is a plus pattern centered at row r, column c.
    The pattern consists of a horizontal line of three 4's at row r, columns c-1 to c+1,
    and single 4's above at r-1,c and below at r+1,c.
    """
    h = len(grid)
    if h == 0:
        return False
    w = len(grid[0])
    if not (1 <= r < h - 1 and 1 <= c < w - 1):
        return False
    return (grid[r][c - 1] == 4 and
            grid[r][c] == 4 and
            grid[r][c + 1] == 4 and
            grid[r - 1][c] == 4 and
            grid[r + 1][c] == 4)

def fill_plus_pattern(output: List[List[int]], r: int, c: int) -> None:
    """
    Fills the plus pattern centered at row r, column c with 8's in the output grid.
    Fills the five positions: (r-1,c), (r,c-1), (r,c), (r,c+1), (r+1,c).
    """
    output[r - 1][c] = 8
    output[r][c - 1] = 8
    output[r][c] = 8
    output[r][c + 1] = 8
    output[r + 1][c] = 8

def program(g: List[List[int]]) -> List[List[int]]:
    """
    Applies the plus pattern filling rule to the input grid.
    Detects all plus patterns based on original grid and fills them with 8's.
    """
    h = len(g)
    if h == 0:
        return []
    w = len(g[0])
    output = [row[:] for row in g]
    for r in range(1, h - 1):
        for c in range(1, w - 1):
            if has_plus_pattern(g, r, c):
                fill_plus_pattern(output, r, c)
    return output
```