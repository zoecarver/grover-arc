```python
from typing import List
from collections import deque

def fill_exterior_0s(g: List[List[int]]) -> List[List[int]]:
    n = 16
    h = [row[:] for row in g]
    visited = [[False] * n for _ in range(n)]
    q = deque()
    # Start from top and left border cells that are 0 or 7
    for c in range(n):
        if h[0][c] == 0 or h[0][c] == 7:
            q.append((0, c))
            visited[0][c] = True
    for r in range(n):
        if h[r][0] == 0 or h[r][0] == 7:
            if not visited[r][0]:
                q.append((r, 0))
                visited[r][0] = True
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while q:
        r, c = q.popleft()
        if h[r][c] == 0:
            h[r][c] = 7
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < n and not visited[nr][nc] and h[nr][nc] == 0:
                visited[nr][nc] = True
                q.append((nr, nc))
    return h

def fill_isolated_non7(g: List[List[int]]) -> List[List[int]]:
    n = 16
    h = [row[:] for row in g]
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    changed = True
    while changed:
        changed = False
        for r in range(n):
            for c in range(n):
                if h[r][c] != 0 and h[r][c] != 7:
                    count7 = 0
                    num_adj = 0
                    for dr, dc in dirs:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < n and 0 <= nc < n:
                            num_adj += 1
                            if h[nr][nc] == 7:
                                count7 += 1
                    if count7 >= 3:
                        h[r][c] = 7
                        changed = True
    return h

def program(g: List[List[int]]) -> List[List[int]]:
    filled_0s = fill_exterior_0s(g)
    result = fill_isolated_non7(filled_0s)
    return result
```