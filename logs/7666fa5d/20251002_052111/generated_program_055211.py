```python
from typing import List
from collections import deque
import copy

def is_strict(g: List[List[int]], r: int, c: int, n: int) -> bool:
    if g[r][c] != 8:
        return False
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dr, dc in dirs:
        nr, nc = r + dr, c + dc
        if 0 <= nr < n and 0 <= nc < n and g[nr][nc] != 8:
            return False
    return True

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    result = copy.deepcopy(g)
    visited = [[False] * n for _ in range(n)]
    queue = deque()
    # First flood: start from border strict 8s
    for i in range(n):
        for j in [0, n - 1]:
            if is_strict(g, i, j, n) and not visited[i][j]:
                visited[i][j] = True
                queue.append((i, j))
    for j in range(n):
        for i in [0, n - 1]:
            if is_strict(g, i, j, n) and not visited[i][j]:
                visited[i][j] = True
                queue.append((i, j))
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while queue:
        r, c = queue.popleft()
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < n and not visited[nr][nc] and is_strict(g, nr, nc, n):
                visited[nr][nc] = True
                queue.append((nr, nc))
    # Second flood: adjacent cells connected to visited strict
    queue = deque()
    for i in range(n):
        for j in range(n):
            if g[i][j] == 8 and not is_strict(g, i, j, n) and not visited[i][j]:
                has_visited = False
                for dr, dc in dirs:
                    nr, nc = i + dr, j + dc
                    if 0 <= nr < n and 0 <= nc < n and visited[nr][nc]:
                        has_visited = True
                        break
                if has_visited:
                    visited[i][j] = True
                    queue.append((i, j))
    while queue:
        r, c = queue.popleft()
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < n and not visited[nr][nc] and g[nr][nc] == 8 and not is_strict(g, nr, nc, n):
                visited[nr][nc] = True
                queue.append((nr, nc))
    # Set unvisited 8s to 2
    for i in range(n):
        for j in range(n):
            if g[i][j] == 8 and not visited[i][j]:
                result[i][j] = 2
    return result
```