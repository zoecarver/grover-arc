```python
from typing import List, Tuple
from collections import deque
import math

def extract_specials(g: List[List[int]]) -> List[Tuple[int, int]]:
    n = len(g)
    return [(i, j) for i in range(n) for j in range(n) if g[i][j] != 8]

def compute_centroid(comp: List[Tuple[int, int]]) -> Tuple[float, float]:
    c_row = sum(p[0] for p in comp) / len(comp)
    c_col = sum(p[1] for p in comp) / len(comp)
    return c_row, c_col

def find_start(comp: List[Tuple[int, int]]) -> Tuple[int, int]:
    return min(comp, key=lambda p: (p[1], p[0]))

def polar_key(p: Tuple[int, int], start: Tuple[int, int]) -> Tuple[float, float]:
    dr = p[0] - start[0]
    dc = p[1] - start[1]
    angle = math.atan2(dr, dc)
    dist_sq = dr * dr + dc * dc
    return (angle, dist_sq)

def order_polygon(comp: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    start = find_start(comp)
    others = [p for p in comp if p != start]
    others.sort(key=lambda p: polar_key(p, start))
    return [start] + others

def make_poly(ordered: List[Tuple[int, int]]) -> List[Tuple[float, float]]:
    return [(c + 0.5, r + 0.5) for r, c in ordered]

def point_in_poly(px: float, py: float, poly: List[Tuple[float, float]]) -> bool:
    n = len(poly)
    inside = False
    p1x, p1y = poly[0]
    for i in range(n + 1):
        p2x, p2y = poly[i % n]
        if min(p1y, p2y) < py <= max(p1y, p2y):
            if px <= max(p1x, p2x):
                if p1y != p2y:
                    xinters = (py - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                else:
                    xinters = p1x
                if p1x == p2x or px <= xinters:
                    inside = not inside
        p1x, p1y = p2x, p2y
    return inside

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    new_grid = [row[:] for row in g]
    specials = extract_specials(g)
    visited = set()
    components = []
    dirs = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
    for pos in specials:
        if pos not in visited:
            comp = []
            queue = deque([pos])
            visited.add(pos)
            while queue:
                r, c = queue.popleft()
                comp.append((r, c))
                for dr, dc in dirs:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < n and 0 <= nc < n and (nr, nc) not in visited and g[nr][nc] != 8:
                        visited.add((nr, nc))
                        queue.append((nr, nc))
            if len(comp) >= 3:
                components.append(comp)
    for comp in components:
        ordered = order_polygon(comp)
        poly = make_poly(ordered)
        for r in range(n):
            for c in range(n):
                if new_grid[r][c] == 8:
                    px = c + 0.5
                    py = r + 0.5
                    if point_in_poly(px, py, poly):
                        new_grid[r][c] = 2
    return new_grid
```