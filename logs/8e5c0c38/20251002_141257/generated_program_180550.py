```python
from typing import List
from collections import Counter

def get_background(grid: List[List[int]]) -> int:
    flat = [cell for row in grid for cell in row]
    return Counter(flat).most_common(1)[0][0]

def remove_isolated(grid: List[List[int]], background: int) -> List[List[int]]:
    n = len(grid)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    new_grid = [row[:] for row in grid]
    for i in range(n):
        for j in range(n):
            if grid[i][j] != background:
                c = grid[i][j]
                neighbors = sum(1 for di, dj in directions if 0 <= i + di < n and 0 <= j + dj < n and grid[i + di][j + dj] == c)
                if neighbors == 0:
                    new_grid[i][j] = background
    return new_grid

def program(g: List[List[int]]) -> List[List[int]]:
    background = get_background(g)
    return remove_isolated(g, background)
```