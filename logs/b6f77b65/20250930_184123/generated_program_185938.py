```python
import copy
from typing import List, Set, Tuple

def get_neighbors(r: int, c: int, rows: int, cols: int) -> List[Tuple[int, int]]:
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    neighbors = []
    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            neighbors.append((nr, nc))
    return neighbors

def find_component(g: List[List[int]], r: int, c: int, target_color: int, visited: Set[Tuple[int, int]]) -> List[Tuple[int, int]]:
    stack = [(r, c)]
    component = []
    while stack:
        cr, cc = stack.pop()
        if (cr, cc) in visited or g[cr][cc] != target_color:
            continue
        visited.add((cr, cc))
        component.append((cr, cc))
        for nr, nc in get_neighbors(cr, cc, len(g), len(g[0])):
            stack.append((nr, nc))
    return component

def remove_large_groups(g: List[List[int]], color: int) -> bool:
    rows = len(g)
    cols = len(g[0])
    visited: Set[Tuple[int, int]] = set()
    removed = False
    for i in range(rows):
        for j in range(cols):
            if g[i][j] == color and (i, j) not in visited:
                component = find_component(g, i, j, color, visited)
                if len(component) >= 3:
                    for x, y in component:
                        g[x][y] = 0
                    removed = True
    return removed

def pack_column_from_bottom(g: List[List[int]], c: int):
    rows = len(g)
    non_zeros = [g[r][c] for r in range(rows) if g[r][c] != 0]
    for r in range(rows):
        if r < rows - len(non_zeros):
            g[r][c] = 0
        else:
            g[r][c] = non_zeros[r - (rows - len(non_zeros))]

def apply_packing_gravity(g: List[List[int]]):
    cols = len(g[0])
    for c in range(cols):
        pack_column_from_bottom(g, c)

def program(g: List[List[int]]) -> List[List[int]]:
    h = copy.deepcopy(g)
    color = h[0][0]
    removed = remove_large_groups(h, color)
    if removed:
        apply_packing_gravity(h)
    return h
```