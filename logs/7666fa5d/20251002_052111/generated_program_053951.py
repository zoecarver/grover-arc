```python
import copy
from typing import List, Tuple

def collect_special_positions(g: List[List[int]]) -> List[Tuple[int, int]]:
    positions = []
    for i in range(len(g)):
        for j in range(len(g[0])):
            if g[i][j] != 8:
                positions.append((i, j))
    positions.sort()  # sorts by row then column
    return positions

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
    vertices = collect_special_positions(g)
    if len(vertices) < 3:
        return copy.deepcopy(g)
    new_g = copy.deepcopy(g)
    rows = len(g)
    cols = len(g[0])
    for i in range(rows):
        for j in range(cols):
            if g[i][j] == 8:
                if point_inside_polygon((i + 0.5, j + 0.5), vertices):
                    new_g[i][j] = 2
    return new_g
```