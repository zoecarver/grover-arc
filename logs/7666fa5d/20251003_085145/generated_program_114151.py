```python
from typing import List
from collections import deque

def is_border(r: int, c: int, n: int) -> bool:
    return r == 0 or r == n - 1 or c == 0 or c == n - 1

def is_blocked(cr: int, cc: int, dr: int, dc: int, g: List[List[int]], n: int, nr: int, nc: int) -> bool:
    if dr != 0:  # vertical move
        left_from = g[cr][cc - 1] if cc > 0 else 8
        right_from = g[cr][cc + 1] if cc < n - 1 else 8
        return left_from != 8 or right_from != 8
    else:  # horizontal move
        upper_from = g[cr - 1][cc] if cr > 0 else 8
        lower_from = g[cr + 1][cc] if cr < n - 1 else 8
        upper_to = g[nr - 1][nc] if nr > 0 else 8
        lower_to = g[nr + 1][nc] if nr < n - 1 else 8
        return upper_from != 8 or lower_from != 8 or upper_to != 8 or lower_to != 8

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    visited = set()
    queue = deque()
    for r in range(n):
        for c in range(n):
            if is_border(r, c, n) and g[r][c] == 8:
                queue.append((r, c))
                visited.add((r, c))
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while queue:
        cr, cc = queue.popleft()
        for dr, dc in dirs:
            nr = cr + dr
            nc = cc + dc
            if 0 <= nr < n and 0 <= nc < n and g[nr][nc] == 8 and (nr, nc) not in visited:
                if not is_blocked(cr, cc, dr, dc, g, n, nr, nc):
                    visited.add((nr, nc))
                    queue.append((nr, nc))
    new_grid = [row[:] for row in g]
    for r in range(n):
        for c in range(n):
            if new_grid[r][c] == 8 and (r, c) not in visited:
                new_grid[r][c] = 2
    return new_grid
```