```python
from typing import List, Tuple, Set
from copy import deepcopy

def get_neighbors(r: int, c: int, rows: int, cols: int) -> List[Tuple[int, int]]:
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # 4-way connectivity
    neighbors = []
    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            neighbors.append((nr, nc))
    return neighbors

def find_connected_component(g: List[List[int]], start_r: int, start_c: int) -> List[Tuple[int, int]]:
    if not g or g[start_r][start_c] == 0:
        return []
    rows, cols = len(g), len(g[0])
    color = g[start_r][start_c]
    visited: Set[Tuple[int, int]] = set()
    stack: List[Tuple[int, int]] = [(start_r, start_c)]
    component: List[Tuple[int, int]] = []
    while stack:
        cr, cc = stack.pop()
        if (cr, cc) in visited or g[cr][cc] != color:
            continue
        visited.add((cr, cc))
        component.append((cr, cc))
        for nr, nc in get_neighbors(cr, cc, rows, cols):
            if (nr, nc) not in visited and g[nr][nc] == color:
                stack.append((nr, nc))
    return component

def remove_component_cells(g: List[List[int]], component: List[Tuple[int, int]]) -> None:
    for r, c in component:
        g[r][c] = 0

def pack_column_from_bottom(g: List[List[int]], col: int) -> None:
    rows = len(g)
    non_zeros = [g[r][col] for r in range(rows) if g[r][col] != 0]
    for r in range(rows):
        if r < rows - len(non_zeros):
            g[r][col] = 0
        else:
            g[r][col] = non_zeros[r - (rows - len(non_zeros))]

def apply_gravity_packing(g: List[List[int]]) -> None:
    if not g or not g[0]:
        return
    cols = len(g[0])
    for c in range(cols):
        pack_column_from_bottom(g, c)

def program(g: List[List[int]]) -> List[List[int]]:
    h = deepcopy(g)
    if not h or not h[0]:
        return g
    C = h[0][0]
    if C == 0:
        return g
    component = find_connected_component(h, 0, 0)
    to_remove = []
    if len(component) >= 3:
        to_remove = component
    else:
        visited = set(component)
        for r in range(len(h)):
            for c in range(len(h[0])):
                if h[r][c] == C and (r, c) not in visited:
                    comp = find_connected_component(h, r, c)
                    if len(comp) >= 3:
                        to_remove += comp
                    visited.update(comp)
    remove_component_cells(h, to_remove)
    apply_gravity_packing(h)
    if len(component) < 3:
        h[0][0] = C
        if len(h) > 0:
            h[-1][0] = 0
    return h
```