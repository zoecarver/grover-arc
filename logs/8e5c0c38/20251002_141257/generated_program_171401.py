```python
from typing import List, Tuple
from collections import Counter, deque

def get_background(g: List[List[int]]) -> int:
    flat = [g[i][j] for i in range(len(g)) for j in range(len(g[0]))]
    return Counter(flat).most_common(1)[0][0]

def get_eight_directions() -> List[Tuple[int, int]]:
    return [(di, dj) for di in [-1, 0, 1] for dj in [-1, 0, 1] if not (di == 0 and dj == 0)]

def count_eight_neighbors(g: List[List[int]], i: int, j: int, c: int) -> int:
    h, w = len(g), len(g[0])
    count = 0
    for di, dj in get_eight_directions():
        ni, nj = i + di, j + dj
        if 0 <= ni < h and 0 <= nj < w and g[ni][nj] == c:
            count += 1
    return count

def flood_fill_eight_connect(g: List[List[int]], start_i: int, start_j: int, c: int, visited: List[List[bool]], h: int, w: int) -> Tuple[List[Tuple[int, int]], int]:
    directions = get_eight_directions()
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
    bg = get_background(g)
    h, w = len(g), len(g[0])
    out = [row[:] for row in g]
    visited = [[False] * w for _ in range(h)]
    for i in range(h):
        for j in range(w):
            if not visited[i][j] and g[i][j] != bg:
                component, size = flood_fill_eight_connect(g, i, j, g[i][j], visited, h, w)
                for pi, pj in component:
                    if count_eight_neighbors(g, pi, pj, g[pi][pj]) < 3:
                        out[pi][pj] = bg
    return out
```