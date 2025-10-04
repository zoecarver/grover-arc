```python
from typing import List
from collections import deque

def is_border(r: int, c: int, n: int) -> bool:
    return r == 0 or r == n - 1 or c == 0 or c == n - 1

def is_move_blocked(r: int, c: int, nr: int, nc: int, grid: List[List[int]], n: int) -> bool:
    dr = nr - r
    dc = nc - c
    if dc == 1:  # right
        # upper diagonal
        if r - 1 >= 0 and grid[r - 1][c] != 8 and grid[r - 1][nc] != 8:
            return True
        # lower diagonal
        if r + 1 < n and grid[r + 1][c] != 8 and grid[r + 1][nc] != 8:
            return True
    elif dc == -1:  # left
        # upper diagonal
        if r - 1 >= 0 and grid[r - 1][nc] != 8 and grid[r - 1][c] != 8:
            return True
        # lower diagonal
        if r + 1 < n and grid[r + 1][nc] != 8 and grid[r + 1][c] != 8:
            return True
    elif dr == 1:  # down
        # left diagonal
        if c - 1 >= 0 and grid[r][c - 1] != 8 and grid[nr][c - 1] != 8:
            return True
        # right diagonal
        if c + 1 < n and grid[r][c + 1] != 8 and grid[nr][c + 1] != 8:
            return True
    elif dr == -1:  # up
        # left diagonal
        if c - 1 >= 0 and grid[nr][c - 1] != 8 and grid[r][c - 1] != 8:
            return True
        # right diagonal
        if c + 1 < n and grid[nr][c + 1] != 8 and grid[r][c + 1] != 8:
            return True
    return False

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    visited: set = set()
    queue = deque()
    for r in range(n):
        for c in range(n):
            if is_border(r, c, n) and g[r][c] == 8:
                queue.append((r, c))
                visited.add((r, c))
    while queue:
        cr, cc = queue.popleft()
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr = cr + dr
            nc = cc + dc
            if 0 <= nr < n and 0 <= nc < n and (nr, nc) not in visited and g[nr][nc] == 8:
                if not is_move_blocked(cr, cc, nr, nc, g, n):
                    visited.add((nr, nc))
                    queue.append((nr, nc))
    new_grid = [row[:] for row in g]
    for r in range(n):
        for c in range(n):
            if new_grid[r][c] == 8 and (r, c) not in visited:
                new_grid[r][c] = 2
    return new_grid
```