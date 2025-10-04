```python
from typing import List, Tuple
from collections import deque
import math
import copy

def get_special_color(g: List[List[int]]) -> int:
    for row in g:
        for cell in row:
            if cell != 8:
                return cell
    return 8

def find_connected_components(g: List[List[int]], special: int, n: int) -> List[List[Tuple[int, int]]]:
    visited = [[False] * n for _ in range(n)]
    components = []
    eight_dirs = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for i in range(n):
        for j in range(n):
            if g[i][j] == special and not visited[i][j]:
                comp = []
                q = deque([(i, j)])
                visited[i][j] = True
                while q:
                    r, c = q.popleft()
                    comp.append((r, c))
                    for dr, dc in eight_dirs:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < n and 0 <= nc < n and g[nr][nc] == special and not visited[nr][nc]:
                            visited[nr][nc] = True
                            q.append((nr, nc))
                components.append(comp)
    return components

def point_inside_polygon(x: float, y: float, vertices: List[Tuple[int, int]]) -> bool:
    n = len(vertices)
    inside = False
    p1x, p1y = float(vertices[0][1]), float(vertices[0][0])
    for i in range(n + 1):
        p2 = vertices[i % n]
        p2x, p2y = float(p2[1]), float(p2[0])
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
    n = len(g)
    special = get_special_color(g)
    if special == 8:
        return copy.deepcopy(g)
    components = find_connected_components(g, special, n)
    out = copy.deepcopy(g)
    for comp in components:
        if len(comp) < 3:
            continue
        sum_r = sum(r for r, _ in comp)
        sum_c = sum(c for _, c in comp)
        cent_r = sum_r / len(comp)
        cent_c = sum_c / len(comp)
        def angle_key(p: Tuple[int, int]) -> float:
            r, c = p
            return math.atan2(r - cent_r, c - cent_c)
        poly = sorted(comp, key=angle_key)
        for i in range(n):
            for j in range(n):
                if g[i][j] == 8 and point_inside_polygon(j + 0.5, i + 0.5, poly):
                    out[i][j] = 2
    return out
```