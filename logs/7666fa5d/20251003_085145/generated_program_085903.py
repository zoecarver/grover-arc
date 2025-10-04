```python
import math
from typing import List
from collections import defaultdict

def program(g: List[List[int]]) -> List[List[int]]:
    n = 16
    out = [row[:] for row in g]
    specials: List[tuple[int, int]] = [(i, j) for i in range(n) for j in range(n) if g[i][j] != 8]
    if not specials:
        return out
    m = len(specials)
    parent = {specials[k]: specials[k] for k in range(m)}
    rank = {specials[k]: 0 for k in range(m)}

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x, y):
        px = find(x)
        py = find(y)
        if px != py:
            if rank[px] < rank[py]:
                parent[px] = py
            elif rank[px] > rank[py]:
                parent[py] = px
            else:
                parent[py] = px
                rank[px] += 1

    for a in range(m):
        for b in range(a + 1, m):
            p1 = specials[a]
            p2 = specials[b]
            dist = abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
            if 1 <= dist <= 4:
                union(p1, p2)

    comp_dict = defaultdict(list)
    for p in specials:
        comp_dict[find(p)].append(p)
    components = [comp for comp in comp_dict.values() if len(comp) >= 3]

    polys = []
    for comp in components:
        c_row = sum(p[0] for p in comp) / len(comp)
        c_col = sum(p[1] for p in comp) / len(comp)
        def get_angle(p: tuple[int, int]) -> float:
            dr = p[0] - c_row
            dc = p[1] - c_col
            return math.atan2(dr, dc)
        sorted_comp = sorted(comp, key=get_angle)
        poly = [(p[1], p[0]) for p in sorted_comp]  # (x=col, y=row)
        polys.append(poly)

    def point_in_poly(px: float, py: float, poly: List[tuple[float, float]]) -> bool:
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

    for i in range(n):
        for j in range(n):
            if out[i][j] != 8:
                continue
            px = j + 0.5
            py = i + 0.5
            for poly in polys:
                if point_in_poly(px, py, poly):
                    out[i][j] = 2
                    break
    return out
```