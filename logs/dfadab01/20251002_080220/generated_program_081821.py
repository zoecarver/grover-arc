```python
from typing import List

def place_vertical_inner(grid: List[List[int]], r: int, c: int, color: int) -> None:
    size = 4
    h = len(grid)
    w = len(grid[0])
    # top sides
    if r < h and c < w:
        grid[r][c] = color
    if r < h and c + 3 < w:
        grid[r][c + 3] = color
    # middle full inner
    if r + 1 < h and c + 1 < w:
        grid[r + 1][c + 1] = color
    if r + 1 < h and c + 2 < w:
        grid[r + 1][c + 2] = color
    if r + 2 < h and c + 1 < w:
        grid[r + 2][c + 1] = color
    if r + 2 < h and c + 2 < w:
        grid[r + 2][c + 2] = color
    # bottom sides
    if r + 3 < h and c < w:
        grid[r + 3][c] = color
    if r + 3 < h and c + 3 < w:
        grid[r + 3][c + 3] = color

def copy_existing_patterns(grid: List[List[int]], out: List[List[int]]) -> None:
    h = len(grid)
    w = len(grid[0])
    for i in range(h):
        for j in range(w):
            if grid[i][j] == 7:
                out[i][j] = 7

def place_for_seeds(grid: List[List[int]], out: List[List[int]]) -> None:
    h = len(grid)
    w = len(grid[0])
    for i in range(h):
        for j in range(w):
            if grid[i][j] == 8:
                place_vertical_inner(out, i, j, 7)

def program(g: List[List[int]]) -> List[List[int]]:
    h = len(g)
    w = len(g[0])
    out = [[0 for _ in range(w)] for _ in range(h)]
    copy_existing_patterns(g, out)
    place_for_seeds(g, out)
    return out
```