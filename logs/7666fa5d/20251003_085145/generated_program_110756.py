```python
from typing import List
from collections import deque

def is_border(r: int, c: int, n: int) -> bool:
    return r == 0 or r == n - 1 or c == 0 or c == n - 1

def is_move_blocked(fr: int, fc: int, tr: int, tc: int, g: List[List[int]], n: int) -> bool:
    dr = tr - fr
    dc = tc - fc
    sides = []
    if dc == 0:  # vertical move
        sides = [
            (fr, fc - 1),
            (fr, fc + 1),
            (tr, tc - 1),
            (tr, tc + 1)
        ]
    else:  # horizontal move
        sides = [
            (fr - 1, fc),
            (fr - 1, tc),
            (fr + 1, fc),
            (fr + 1, tc)
        ]
    for sr, sc in sides:
        if 0 <= sr < n and 0 <= sc < n and g[sr][sc] != 8:
            return True
    return False

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
            nr, nc = cr + dr, cc + dc
            if 0 <= nr < n and 0 <= nc < n and g[nr][nc] == 8 and (nr, nc) not in visited:
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