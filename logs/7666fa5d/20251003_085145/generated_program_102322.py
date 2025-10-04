```python
import math
from typing import List, Tuple

def find(parent: List[int], x: int) -> int:
    root = x
    while parent[root] != root:
        root = parent[root]
    # path compression
    while x != root:
        next_x = parent[x]
        parent[x] = root
        x = next_x
    return root

def group_singles(positions: List[Tuple[int, int]], dist_threshold: float = 5.0) -> List[List[Tuple[int, int]]]:
    n = len(positions)
    if n == 0:
        return []
    parent = list(range(n))
    for a in range(n):
        for b in range(a + 1, n):
            i1, j1 = positions[a]
            i2, j2 = positions[b]
            d = math.sqrt((i1 - i2) ** 2 + (j1 - j2) ** 2)
            if d <= dist_threshold:
                pa = find(parent, a)
                pb = find(parent, b)
                if pa != pb:
                    parent[pa] = pb
    groups_dict = {}
    for k in range(n):
        p = find(parent, k)
        if p not in groups_dict:
            groups_dict[p] = []
        groups_dict[p].append(positions[k])
    return [g for g in groups_dict.values() if len(g) >= 2]

def compute_polygon(group: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    num = len(group)
    if num < 3:
        return []
    sum_i = sum(p[0] for p in group)
    sum_j = sum(p[1] for p in group)
    c_i = sum_i / num
    c_j = sum_j / num
    def get_angle(p: Tuple[int, int]) -> float:
        d_i = p[0] - c_i
        d_j = p[1] - c_j
        return math.atan2(d_j, d_i)
    sorted_group = sorted(group, key=get_angle)
    return sorted_group

def point_in_poly(x: float, y: float, poly: List[Tuple[float, float]]) -> bool:
    n = len(poly)
    inside = False
    p1x, p1y = poly[0]
    for i in range(1, n + 1):
        p2x, p2y = poly[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside

def program(g: List[List[int]]) -> List[List[int]]:
    SIZE = 16
    grid = [row[:] for row in g]
    special_pos = [(i, j) for i in range(SIZE) for j in range(SIZE) if g[i][j] != 8]
    groups = group_singles(special_pos)
    polys = []
    for group in groups:
        poly = compute_polygon(group)
        if poly:
            # poly_points: list of (x=col j, y=row i)
            poly_points = [(p[1], p[0]) for p in poly]
            polys.append(poly_points)
    for i in range(SIZE):
        for j in range(SIZE):
            if g[i][j] == 8:
                for poly in polys:
                    if point_in_poly(float(j), float(i), poly):
                        grid[i][j] = 2
                        break
    return grid
```