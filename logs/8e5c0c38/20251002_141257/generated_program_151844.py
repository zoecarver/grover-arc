```python
from typing import List, Tuple
from collections import Counter, deque

def get_background(g: List[List[int]]) -> int:
    flat = [g[i][j] for i in range(22) for j in range(22)]
    return Counter(flat).most_common(1)[0][0]

def get_directions() -> List[Tuple[int, int]]:
    dirs = []
    for di in [-1, 0, 1]:
        for dj in [-1, 0, 1]:
            if di == 0 and dj == 0:
                continue
            dirs.append((di, dj))
    return dirs

def flood_fill_component(g: List[List[int]], start_i: int, start_j: int, c: int, visited: List[List[bool]], h: int, w: int) -> Tuple[List[Tuple[int, int]], int]:
    directions = get_directions()
    component = []
    queue = deque([(start_i, start_j)])
    visited[start_i][start_j] = True
    size = 1
    component.append((start_i, start_j))
    
    while queue:
        i, j = queue.popleft()
        for di, dj in directions:
            ni, nj = i + di, j + dj
            if 0 <= ni < h and 0 <= nj < w and not visited[ni][nj] and g[ni][nj] == c:
                visited[ni][nj] = True
                queue.append((ni, nj))
                component.append((ni, nj))
                size += 1
    return component, size

def program(g: List[List[int]]) -> List[List[int]]:
    h = 22
    w = 22
    bg = get_background(g)
    out = [row[:] for row in g]
    visited = [[False] * w for _ in range(h)]
    for i in range(h):
        for j in range(w):
            if g[i][j] != bg and not visited[i][j]:
                component, size = flood_fill_component(g, i, j, g[i][j], visited, h, w)
                if size < 3:
                    for x, y in component:
                        out[x][y] = bg
    return out
```