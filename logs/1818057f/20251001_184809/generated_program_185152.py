```python
from typing import List

def is_interior(grid: List[List[int]], i: int, j: int, rows: int, cols: int) -> bool:
    if not (0 < i < rows - 1 and 0 < j < cols - 1):
        return False
    if grid[i][j] != 4:
        return False
    return (grid[i - 1][j] == 4 and
            grid[i + 1][j] == 4 and
            grid[i][j - 1] == 4 and
            grid[i][j + 1] == 4)

def fill_cross(output: List[List[int]], i: int, j: int, rows: int, cols: int) -> None:
    positions = [(i, j), (i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]
    for x, y in positions:
        if 0 <= x < rows and 0 <= y < cols and output[x][y] == 4:
            output[x][y] = 8

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    rows = len(g)
    cols = len(g[0])
    output = [row[:] for row in g]
    for i in range(1, rows - 1):
        for j in range(1, cols - 1):
            if is_interior(g, i, j, rows, cols):
                fill_cross(output, i, j, rows, cols)
    return output
```