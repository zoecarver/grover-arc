```python
from typing import List
from collections import deque
import copy

def get_positive_colors(g: List[List[int]]) -> List[int]:
    colors = set()
    for row in g:
        for val in row:
            if val > 0:
                colors.add(val)
    return sorted(list(colors))

def get_sources(g: List[List[int]], color: int, rows: int, cols: int) -> List[tuple]:
    sources = []
    for r in range(rows):
        for c in range(cols):
            if g[r][c] == color:
                sources.append((r, c))
    return sources

def compute_dist(g: List[List[int]], sources: List[tuple], traversable: set, rows: int, cols: int) -> List[List[float]]:
    dist = [[float('inf')] * cols for _ in range(rows)]
    q = deque()
    visited = [[False] * cols for _ in range(rows)]
    for r, c in sources:
        dist[r][c] = 0.0
        q.append((r, c))
        visited[r][c] = True
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    while q:
        cr, cc = q.popleft()
        for dr, dc in directions:
            nr, nc = cr + dr, cc + dc
            if 0 <= nr < rows and 0 <= nc < cols and not visited[nr][nc] and g[nr][nc] in traversable:
                visited[nr][nc] = True
                dist[nr][nc] = dist[cr][cc] + 1
                q.append((nr, nc))
    return dist

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return g
    rows = len(g)
    cols = len(g[0])
    positive_colors = get_positive_colors(g)
    num_colors = len(positive_colors)
    if num_colors < 3:
        return [row[:] for row in g]
    border1 = positive_colors[0]
    border2 = positive_colors[1]
    target = positive_colors[2]
    traversable = {border1, border2, target}
    sources1 = get_sources(g, border1, rows, cols)
    sources2 = get_sources(g, border2, rows, cols)
    dist1 = compute_dist(g, sources1, traversable, rows, cols)
    dist2 = compute_dist(g, sources2, traversable, rows, cols)
    new_g = [row[:] for row in g]
    half = rows // 2
    for r in range(rows):
        for c in range(cols):
            if g[r][c] != target:
                continue
            d1 = dist1[r][c]
            d2 = dist2[r][c]
            if d1 == float('inf') and d2 == float('inf'):
                continue
            if d1 == float('inf'):
                new_g[r][c] = border2
                continue
            if d2 == float('inf'):
                new_g[r][c] = border1
                continue
            if d1 < d2:
                new_g[r][c] = border1
            elif d2 < d1:
                new_g[r][c] = border2
            else:
                if d1 == 1:
                    if r < half:
                        new_g[r][c] = border1
                    else:
                        new_g[r][c] = border2
                # else tie at larger d, stay target
    return new_g
```