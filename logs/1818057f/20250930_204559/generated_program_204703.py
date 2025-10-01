```python
from typing import List

def copy_grid(grid: List[List[int]]) -> List[List[int]]:
    return [row[:] for row in grid]

def is_pattern_start(grid: List[List[int]], i: int, j: int) -> bool:
    rows = len(grid)
    cols = len(grid[0]) if grid else 0
    if i + 2 >= rows or j - 1 < 0 or j + 1 >= cols:
        return False
    return (grid[i][j] == 4 and
            grid[i + 1][j - 1] == 4 and
            grid[i + 1][j] == 4 and
            grid[i + 1][j + 1] == 4 and
            grid[i + 2][j] == 4)

def apply_pattern(grid: List[List[int]], i: int, j: int) -> None:
    grid[i][j] = 8
    grid[i + 1][j - 1] = 8
    grid[i + 1][j] = 8
    grid[i + 1][j + 1] = 8
    grid[i + 2][j] = 8

def find_and_apply_patterns(grid: List[List[int]]) -> None:
    rows = len(grid)
    cols = len(grid[0]) if grid else 0
    for i in range(rows - 2):
        for j in range(1, cols - 1):
            if is_pattern_start(grid, i, j):
                apply_pattern(grid, i, j)

def program(g: List[List[int]]) -> List[List[int]]:
    output = copy_grid(g)
    find_and_apply_patterns(output)
    return output
```