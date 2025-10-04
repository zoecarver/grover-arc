```python
from typing import List, Tuple
from collections import deque
import math

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

def point_inside_polygon(point: Tuple[float, float], vertices: List[Tuple[int, int]]) -> bool:
    x, y = point
    n = len(vertices)
    inside = False
    p1x, p1y = vertices[0]
    for i in range(n + 1):
        p2x, p2y = vertices[i % n]
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
        return [row[:] for row in g]
    comps = find_connected_components(g, special, n)
    result = [row[:] for row in g]
    for i in range(n):
        for j in range(n):
            if g[i][j] == 8:
                point = (i + 0.5, j + 0.5)
                for comp in comps:
                    if len(comp) < 4:
                        continue
                    cr = sum(rr for rr, cc in comp) / len(comp)
                    cc = sum(cc for rr, cc in comp) / len(comp)
                    def angle_key(p: Tuple[int, int]) -> float:
                        pr, pc = p
                        dy = pr - cr
                        dx = pc - cc
                        return math.atan2(dy, dx)
                    vertices = sorted(comp, key=angle_key)
                    if point_inside_polygon(point, vertices):
                        result[i][j] = 2
                        break
    return result
```