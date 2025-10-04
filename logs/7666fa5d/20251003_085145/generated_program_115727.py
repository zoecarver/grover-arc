```python
from collections import deque
from typing import List

def cell_open(r: int, c: int, g: List[List[int]], n: int) -> bool:
    if not (0 <= r < n and 0 <= c < n):
        return True
    return g[r][c] == 8

def can_move(cr: int, cc: int, nr: int, nc: int, g: List[List[int]], n: int) -> bool:
    dr = nr - cr
    dc = nc - cc
    if abs(dr) == 1 and dc == 0:  # vertical move
        left_open = cell_open(cr, cc - 1, g, n)
        right_open = cell_open(cr, cc + 1, g, n)
        return left_open and right_open
    elif dr == 0 and abs(dc) == 1:  # horizontal move
        # source perpendicular
        up_s_open = cell_open(cr - 1, cc, g, n)
        down_s_open = cell_open(cr + 1, cc, g, n)
        # target perpendicular
        up_t_open = cell_open(nr - 1, nc, g, n)
        down_t_open = cell_open(nr + 1, nc, g, n)
        return up_s_open and down_s_open and up_t_open and down_t_open
    return False

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    visited = set()
    q = deque()
    # Add all border 8's to queue and visited
    for i in range(n):
        if g[0][i] == 8:
            pos = (0, i)
            visited.add(pos)
            q.append(pos)
        if g[n - 1][i] == 8:
            pos = (n - 1, i)
            if pos not in visited:
                visited.add(pos)
                q.append(pos)
    for i in range(n):
        if g[i][0] == 8:
            pos = (i, 0)
            if pos not in visited:
                visited.add(pos)
                q.append(pos)
        if g[i][n - 1] == 8:
            pos = (i, n - 1)
            if pos not in visited:
                visited.add(pos)
                q.append(pos)
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while q:
        cr, cc = q.popleft()
        for dr, dc in dirs:
            nr = cr + dr
            nc = cc + dc
            if 0 <= nr < n and 0 <= nc < n and g[nr][nc] == 8 and (nr, nc) not in visited:
                if can_move(cr, cc, nr, nc, g, n):
                    visited.add((nr, nc))
                    q.append((nr, nc))
    # Create output grid
    out_g = [row[:] for row in g]
    for r in range(n):
        for c in range(n):
            if out_g[r][c] == 8 and (r, c) not in visited:
                out_g[r][c] = 2
    return out_g
```