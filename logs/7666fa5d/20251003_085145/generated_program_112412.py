```python
from collections import deque
from typing import List

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    visited = set()
    q = deque()
    for i in range(n):
        for j in range(n):
            if (i == 0 or i == n - 1 or j == 0 or j == n - 1) and g[i][j] == 8:
                q.append((i, j))
                visited.add((i, j))
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while q:
        cr, cc = q.popleft()
        for dr, dc in dirs:
            nr = cr + dr
            nc = cc + dc
            if 0 <= nr < n and 0 <= nc < n and g[nr][nc] == 8 and (nr, nc) not in visited:
                blocked = False
                if dr == 0:  # horizontal
                    if dc == 1:  # right
                        if 0 <= cr + 1 < n and g[cr + 1][nc] != 8:
                            blocked = True
                        if 0 <= cr - 1 < n and g[cr - 1][cc] != 8:
                            blocked = True
                    else:  # left
                        if 0 <= cr + 1 < n and g[cr + 1][cc] != 8:
                            blocked = True
                        if 0 <= cr - 1 < n and g[cr - 1][nc] != 8:
                            blocked = True
                else:  # vertical
                    if dr == 1:  # down
                        if cr == 0 and ((cc > 0 and g[cr][cc - 1] != 8) or (cc < n - 1 and g[cr][cc + 1] != 8)):
                            blocked = True
                    # up: no block
                if not blocked:
                    visited.add((nr, nc))
                    q.append((nr, nc))
    new_grid = [row[:] for row in g]
    for i in range(n):
        for j in range(n):
            if new_grid[i][j] == 8 and (i, j) not in visited:
                new_grid[i][j] = 2
    return new_grid
```