```python
from typing import List
from collections import deque

def is_non_seven(x: int, y: int, g: List[List[int]], n: int) -> bool:
    return 0 <= x < n and 0 <= y < n and g[x][y] != 7

def touches_top_or_bottom(component: List[tuple], n: int) -> bool:
    for x, y in component:
        if x == 0 or x == n - 1:
            return True
    return False

def flood_component(x: int, y: int, g: List[List[int]], n: int, visited: List[List[bool]]) -> List[tuple]:
    component = []
    q = deque([(x, y)])
    visited[x][y] = True
    while q:
        cx, cy = q.popleft()
        component.append((cx, cy))
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = cx + dx, cy + dy
            if is_non_seven(nx, ny, g, n) and not visited[nx][ny]:
                visited[nx][ny] = True
                q.append((nx, ny))
    return component

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    h = [row[:] for row in g]
    visited = [[False for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if g[i][j] != 7 and not visited[i][j]:
                component = flood_component(i, j, g, n, visited)
                if not touches_top_or_bottom(component, n):
                    for x, y in component:
                        h[x][y] = 7
    return h
```