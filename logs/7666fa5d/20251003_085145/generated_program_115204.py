```python
from typing import List
from collections import deque

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    visited = set()
    queue = deque()
    # Collect border 8's
    for i in range(n):
        if g[0][i] == 8:
            pos = (0, i)
            if pos not in visited:
                visited.add(pos)
                queue.append(pos)
        if g[n-1][i] == 8:
            pos = (n-1, i)
            if pos not in visited:
                visited.add(pos)
                queue.append(pos)
    for i in range(n):
        if g[i][0] == 8:
            pos = (i, 0)
            if pos not in visited:
                visited.add(pos)
                queue.append(pos)
        if g[i][n-1] == 8:
            pos = (i, n-1)
            if pos not in visited:
                visited.add(pos)
                queue.append(pos)
    # BFS flood fill
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while queue:
        r, c = queue.popleft()
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < n and g[nr][nc] == 8 and (nr, nc) not in visited:
                visited.add((nr, nc))
                queue.append((nr, nc))
    # Create output grid
    out = [row[:] for row in g]
    for r in range(n):
        for c in range(n):
            if out[r][c] == 8 and (r, c) not in visited:
                out[r][c] = 2
    return out
```