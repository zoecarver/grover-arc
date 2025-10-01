```python
import collections
from typing import List
from copy import deepcopy

def select_color(i: int) -> int:
    cycle = [4, 3, 1, 2]
    return cycle[i % 4]

def flood_fill(g: List[List[int]], r: int, c: int, col: int, visited: List[List[bool]]) -> None:
    h, w = len(g), len(g[0])
    q = collections.deque([(r, c)])
    visited[r][c] = True
    g[r][c] = col
    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    while q:
        x, y = q.popleft()
        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            if 0 <= nx < h and 0 <= ny < w and g[nx][ny] > 4 and not visited[nx][ny]:
                visited[nx][ny] = True
                g[nx][ny] = col
                q.append((nx, ny))

def program(g: List[List[int]]) -> List[List[int]]:
    g = deepcopy(g)
    h = len(g)
    if h == 0:
        return g
    w = len(g[0])
    visited = [[False] * w for _ in range(h)]
    component_index = 0
    for r in range(h):
        for c in range(w):
            if g[r][c] > 4 and not visited[r][c]:
                col = select_color(component_index)
                flood_fill(g, r, c, col, visited)
                component_index += 1
    return g
```