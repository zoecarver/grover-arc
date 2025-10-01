```python
from typing import List, Tuple, Set
from copy import deepcopy

def get_neighbors(r: int, c: int, rows: int, cols: int) -> List[Tuple[int, int]]:
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
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

def protect_top_left_component(g: List[List[int]], visited: Set[Tuple[int, int]]) -> None:
    if g[0][0] != 0:
        top_component = find_connected_component(g, 0, 0)
        for r, c in top_component:
            visited.add((r, c))

def remove_other_large_groups(g: List[List[int]], C: int, visited: Set[Tuple[int, int]]) -> None:
    rows, cols = len(g), len(g[0])
    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited and g[r][c] == C:
                component = find_connected_component(g, r, c)
                if len(component) >= 3:
                    remove_component_cells(g, component)
                for cell in component:
                    visited.add(cell)

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return g
    h = deepcopy(g)
    C = h[0][0]
    if C == 0:
        return h
    visited = set()
    protect_top_left_component(h, visited)
    remove_other_large_groups(h, C, visited)
    return h
```