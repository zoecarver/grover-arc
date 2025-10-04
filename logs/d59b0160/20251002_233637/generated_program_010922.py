```python
from typing import List
from collections import deque

def copy_grid(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    return [row[:] for row in g]

def fill_exterior_0s(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    h = [row[:] for row in g]
    visited = [[False] * n for _ in range(n)]
    q = deque()
    # Start from all four borders: cells that are 0 or 7
    # Top
    for c in range(n):
        if h[0][c] == 0 or h[0][c] == 7:
            q.append((0, c))
            visited[0][c] = True
    # Bottom
    for c in range(n):
        if h[n-1][c] == 0 or h[n-1][c] == 7:
            if not visited[n-1][c]:
                q.append((n-1, c))
                visited[n-1][c] = True
    # Left (skip corners if already visited)
    for r in range(n):
        if h[r][0] == 0 or h[r][0] == 7:
            if not visited[r][0]:
                q.append((r, 0))
                visited[r][0] = True
    # Right
    for r in range(n):
        if h[r][n-1] == 0 or h[r][n-1] == 7:
            if not visited[r][n-1]:
                q.append((r, n-1))
                visited[r][n-1] = True
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

def program(g: List[List[int]]) -> List[List[int]]:
    h = copy_grid(g)
    h = fill_exterior_0s(h)
    return h
```