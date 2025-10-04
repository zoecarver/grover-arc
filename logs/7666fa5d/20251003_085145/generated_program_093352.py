```python
from typing import List, Tuple
from collections import defaultdict
import math

def extract_specials(g: List[List[int]]) -> List[Tuple[int, int]]:
    n = len(g)
    return [(i, j) for i in range(n) for j in range(n) if g[i][j] != 8]

def manhattan(p1: Tuple[int, int], p2: Tuple[int, int]) -> int:
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def find(parent: dict, x: Tuple[int, int]) -> Tuple[int, int]:
    if parent[x] != x:
        parent[x] = find(parent, parent[x])
    return parent[x]

def union(parent: dict, rank: dict, x: Tuple[int, int], y: Tuple[int, int]):
    px = find(parent, x)
    py = find(parent, y)
    if px != py:
        if rank[px] < rank[py]:
            parent[px] = py
        elif rank[px] > rank[py]:
            parent[py] = px
        else:
            parent[py] = px
            rank[px] += 1

def get_components(specials: List[Tuple[int, int]], threshold: int = 4) -> List[List[Tuple[int, int]]]:
    if not specials:
        return []
    parent = {p: p for p in specials}
    rank = {p: 0 for p in specials}
    for i in range(len(specials)):
        for j in range(i + 1, len(specials)):
            if manhattan(specials[i], specials[j]) <= threshold:
                union(parent, rank, specials[i], specials[j])
    comp_dict = defaultdict(list)
    for p in specials:
        comp_dict[find(parent, p)].append(p)
    return [comp for comp in comp_dict.values() if len(comp) >= 3]

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
    new_grid = [row[:] for row in g]
    specials = extract_specials(g)
    comps = get_components(specials)
    for comp in comps:
        ordered = order_polygon(comp)
        poly = make_poly(ordered)
        for r in range(16):
            for c in range(16):
                if new_grid[r][c] == 8:
                    if point_in_poly(c + 0.5, r + 0.5, poly):
                        new_grid[r][c] = 2
    return new_grid
```