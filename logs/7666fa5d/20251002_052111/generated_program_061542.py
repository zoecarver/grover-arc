```python
from typing import List, Tuple
import math

def find_primary_color(g: List[List[int]]) -> int:
    colors = set(val for row in g for val in row if val != 8)
    if not colors:
        return 8
    return min(colors)

def find_primary_positions(g: List[List[int]], p: int) -> List[Tuple[int, int]]:
    positions = []
    for r in range(16):
        for c in range(16):
            if g[r][c] == p:
                positions.append((r, c))
    return positions

def cluster_points(pos: List[Tuple[int, int]]) -> List[List[Tuple[int, int]]]:
    n = len(pos)
    if n == 0:
        return []
    parent = list(range(n))
    def find(x: int) -> int:
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
    def union(x: int, y: int):
        px = find(x)
        py = find(y)
        if px != py:
            parent[px] = py
    for i in range(n):
        for j in range(i + 1, n):
            r1, c1 = pos[i]
            r2, c2 = pos[j]
            dist = math.sqrt((r1 - r2)**2 + (c1 - c2)**2)
            if dist <= 5.5:
                union(i, j)
    clusters = {}
    for i in range(n):
        root = find(i)
        if root not in clusters:
            clusters[root] = []
        clusters[root].append(pos[i])
    return [cl for cl in clusters.values() if len(cl) >= 3]

def sort_by_angle(pos: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    if len(pos) < 3:
        return pos
    sum_r = sum(r for r, _ in pos)
    sum_c = sum(c for _, c in pos)
    cent_r = sum_r / len(pos)
    cent_c = sum_c / len(pos)
    def angle_key(pt: Tuple[int, int]) -> float:
        r, c = pt
        return math.atan2(r - cent_r, c - cent_c)
    return sorted(pos, key=angle_key)

def point_in_polygon(point: Tuple[int, int], poly: List[Tuple[int, int]]) -> bool:
    x = point[1]  # col as x
    y = point[0]  # row as y
    n = len(poly)
    inside = False
    p1x = poly[0][1]
    p1y = poly[0][0]
    for i in range(1, n + 1):
        p2 = poly[i % n]
        p2x = p2[1]
        p2y = p2[0]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
        p1x = p2x
        p1y = p2y
    return inside

def program(g: List[List[int]]) -> List[List[int]]:
    out_g = [row[:] for row in g]
    p = find_primary_color(g)
    all_pos = find_primary_positions(g, p)
    clusters = cluster_points(all_pos)
    for cluster in clusters:
        poly = sort_by_angle(cluster)
        for r in range(16):
            for c in range(16):
                if out_g[r][c] == 8 and point_in_polygon((r, c), poly):
                    out_g[r][c] = 2
    return out_g
```