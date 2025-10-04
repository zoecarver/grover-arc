```python
from typing import List, Tuple

def flood_fill(g: List[List[int]], start_r: int, start_c: int, visited: List[List[bool]]) -> List[Tuple[int, int]]:
    N = 30
    C = g[start_r][start_c]
    stack: List[Tuple[int, int]] = [(start_r, start_c)]
    component: List[Tuple[int, int]] = []
    visited[start_r][start_c] = True
    while stack:
        i, j = stack.pop()
        component.append((i, j))
        for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ni, nj = i + di, j + dj
            if 0 <= ni < N and 0 <= nj < N and not visited[ni][nj] and g[ni][nj] == C:
                visited[ni][nj] = True
                stack.append((ni, nj))
    return component

def compute_h(g: List[List[int]], component: List[Tuple[int, int]]) -> int:
    N = 30
    comp_set = set(component)
    h = 0
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(N):
        for j in range(N):
            if g[i][j] == 0:
                neigh_pos = [(i + di, j + dj) for di, dj in dirs]
                if all(0 <= ni < N and 0 <= nj < N and (ni, nj) in comp_set for ni, nj in neigh_pos):
                    h += 1
    return h

def identify_keys(g: List[List[int]]) -> dict:
    N = 30
    visited = [[False] * N for _ in range(N)]
    mapping: dict = {}
    for r in range(N):
        for c in range(N):
            if g[r][c] != 0 and g[r][c] != 5 and not visited[r][c]:
                component = flood_fill(g, r, c, visited)
                if component:
                    minr = min(x for x, _ in component)
                    maxr = max(x for x, _ in component)
                    if maxr - minr + 1 == 3:
                        C = g[r][c]
                        h = compute_h(g, component)
                        mapping[h] = C
    return mapping

def transform_fives(g: List[List[int]], mapping: dict, output: List[List[int]]):
    N = 30
    visited = [[False] * N for _ in range(N)]
    for r in range(N):
        for c in range(N):
            if g[r][c] == 5 and not visited[r][c]:
                component = flood_fill(g, r, c, visited)
                if component:
                    h = compute_h(g, component)
                    new_c = mapping.get(h, 0)
                    for x, y in component:
                        output[x][y] = new_c

def program(g: List[List[int]]) -> List[List[int]]:
    output = [row[:] for row in g]
    mapping = identify_keys(g)
    transform_fives(g, mapping, output)
    return output
```