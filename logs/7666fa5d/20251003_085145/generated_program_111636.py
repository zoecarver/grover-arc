```python
import math
from collections import deque
from typing import List, Tuple

def get_components(g: List[List[int]], c: int) -> List[List[Tuple[int, int]]]:
    h = len(g)
    w = len(g[0])
    visited = [[False] * w for _ in range(h)]
    components = []
    dirs = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for i in range(h):
        for j in range(w):
            if g[i][j] == c and not visited[i][j]:
                comp = []
                q = deque([(i, j)])
                visited[i][j] = True
                while q:
                    x, y = q.popleft()
                    comp.append((x, y))
                    for dx, dy in dirs:
                        nx = x + dx
                        ny = y + dy
                        if 0 <= nx < h and 0 <= ny < w and g[nx][ny] == c and not visited[nx][ny]:
                            visited[nx][ny] = True
                            q.append((nx, ny))
                components.append(comp)
    return components

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return [row[:] for row in g]
    h = len(g)
    w = len(g[0])
    colors = set()
    for row in g:
        for val in row:
            if val != 0:
                colors.add(val)
    if not colors:
        return [row[:] for row in g]
    c = max(colors)
    components = get_components(g, c)
    new_g = [row[:] for row in g]
    for comp in components:
        if len(comp) < 3:
            continue
        cy = sum(p[0] for p in comp) / len(comp)
        cx = sum(p[1] for p in comp) / len(comp)
        def angle_key(p: Tuple[int, int]) -> float:
            return math.atan2(p[1] - cx, p[0] - cy)
        comp.sort(key=angle_key)
        edges = []
        n = len(comp)
        for k in range(n):
            p1 = comp[k]
            p2 = comp[(k + 1) % n]
            edges.append((p1, p2))
        min_r = min(p[0] for p in comp)
        max_r = max(p[0] for p in comp)
        for i in range(min_r, max_r + 1):
            inters = []
            for (r1, c1), (r2, c2) in edges:
                if r1 == r2:
                    continue
                if r1 > r2:
                    r1, r2 = r2, r1
                    c1, c2 = c2, c1
                if r1 <= i < r2:
                    f = (i - r1) / (r2 - r1)
                    ci = c1 + f * (c2 - c1)
                    inters.append(ci)
            if inters:
                inters.sort()
                for k in range(0, len(inters) - 1, 2):
                    left = math.ceil(inters[k])
                    right = math.floor(inters[k + 1])
                    for j in range(max(0, left), min(w, right + 1)):
                        if new_g[i][j] == 0:
                            new_g[i][j] = 1
    return new_g
```