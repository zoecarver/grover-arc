```python
from typing import List
from collections import deque

def get_background_visited(g: List[List[int]]) -> List[List[bool]]:
    n = len(g)
    def is_valid(i: int, j: int) -> bool:
        return 0 <= i < n and 0 <= j < n
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    visited = [[False] * n for _ in range(n)]
    q = deque()
    # Enqueue border 8's
    for i in range(n):
        if g[i][0] == 8:
            q.append((i, 0))
            visited[i][0] = True
        if g[i][n - 1] == 8:
            q.append((i, n - 1))
            visited[i][n - 1] = True
    for j in range(n):
        if g[0][j] == 8 and not visited[0][j]:
            q.append((0, j))
            visited[0][j] = True
        if g[n - 1][j] == 8 and not visited[n - 1][j]:
            q.append((n - 1, j))
            visited[n - 1][j] = True
    while q:
        x, y = q.popleft()
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if is_valid(nx, ny) and not visited[nx][ny] and g[nx][ny] == 8:
                visited[nx][ny] = True
                q.append((nx, ny))
    return visited

def create_output(g: List[List[int]], visited: List[List[bool]]) -> List[List[int]]:
    n = len(g)
    output = [row[:] for row in g]
    for i in range(n):
        for j in range(n):
            if g[i][j] == 8 and not visited[i][j]:
                output[i][j] = 2
    return output

def program(g: List[List[int]]) -> List[List[int]]:
    visited = get_background_visited(g)
    return create_output(g, visited)
```