```python
from collections import deque
from typing import List

def mark_outside_regions(g: List[List[int]]) -> List[List[bool]]:
    n = 16
    visited = [[False] * n for _ in range(n)]
    q = deque()
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    # Enqueue border zero cells
    for r in range(n):
        for c in (0, n - 1):
            if g[r][c] == 0 and not visited[r][c]:
                visited[r][c] = True
                q.append((r, c))
    for c in range(n):
        for r in (0, n - 1):
            if g[r][c] == 0 and not visited[r][c]:
                visited[r][c] = True
                q.append((r, c))
    # Propagate to reachable zero cells using 4-connectivity
    while q:
        r, c = q.popleft()
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < n and g[nr][nc] == 0 and not visited[nr][nc]:
                visited[nr][nc] = True
                q.append((nr, nc))
    return visited

def fill_enclosed_regions(g: List[List[int]], outside_mask: List[List[bool]]) -> List[List[int]]:
    n = 16
    output = [row[:] for row in g]
    for r in range(n):
        for c in range(n):
            if g[r][c] == 0 and not outside_mask[r][c]:
                output[r][c] = 1
    return output

def program(g: List[List[int]]) -> List[List[int]]:
    outside = mark_outside_regions(g)
    return fill_enclosed_regions(g, outside)
```