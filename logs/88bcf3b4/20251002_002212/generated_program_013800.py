```python
from typing import List
from collections import Counter

def find_background(g: List[List[int]]) -> int:
    if not g or not g[0]:
        return 0
    flat = [cell for row in g for cell in row]
    return Counter(flat).most_common(1)[0][0]

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    if n == 0:
        return g
    bg = find_background(g)
    grid = [row[:] for row in g]
    for _ in range(n):
        moved = False
        new_grid = [row[:] for row in grid]
        for r in range(n - 1):
            for c in range(n):
                if grid[r][c] != bg:
                    if r + 1 < n and grid[r + 1][c] == bg:
                        new_grid[r + 1][c] = grid[r][c]
                        new_grid[r][c] = bg
                        moved = True
                    elif c < n - 1 and r + 1 < n and grid[r + 1][c + 1] == bg:
                        new_grid[r + 1][c + 1] = grid[r][c]
                        new_grid[r][c] = bg
                        moved = True
                    elif c > 0 and r + 1 < n and grid[r + 1][c - 1] == bg:
                        new_grid[r + 1][c - 1] = grid[r][c]
                        new_grid[r][c] = bg
                        moved = True
        grid = new_grid
        if not moved:
            break
    return grid
```