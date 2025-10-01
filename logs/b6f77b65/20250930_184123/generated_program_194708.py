```python
from typing import List, Tuple, Set
from copy import deepcopy

def get_neighbors(r: int, c: int, rows: int, cols: int) -> List[Tuple[int, int]]:
    # Helper: Get 4-way adjacent neighbors within bounds
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    neighbors = []
    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            neighbors.append((nr, nc))
    return neighbors

def find_connected_component(g: List[List[int]], start_r: int, start_c: int) -> List[Tuple[int, int]]:
    # Rule: Find the 4-way connected component of same color starting from (start_r, start_c) using DFS stack
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
    # Helper: Set all cells in the component to 0 (remove)
    for r, c in component:
        g[r][c] = 0

def pack_column_from_bottom(g: List[List[int]], col: int) -> None:
    # Rule: Pack non-zero cells in the column to the bottom, preserving top-to-bottom order, 0s at top
    rows = len(g)
    non_zeros = [g[r][col] for r in range(rows) if g[r][col] != 0]
    offset = rows - len(non_zeros)
    for r in range(rows):
        if r < offset:
            g[r][col] = 0
        else:
            g[r][col] = non_zeros[r - offset]

def pack_column_special(g: List[List[int]], col: int) -> None:
    # Rule: For column 0, keep row 0 fixed, pack non-zeros from rows 1+ to bottom of rows 1-11 with 0s above in rows 1+; for other columns, full bottom pack
    rows = len(g)
    if col != 0:
        pack_column_from_bottom(g, col)
        return
    # Keep row 0 as is
    non_zeros = [g[r][col] for r in range(1, rows) if g[r][col] != 0]
    len_n = len(non_zeros)
    # Pack into rows 1 to 11 from the bottom (row 12-len_n to row 11, 0s in row 1 to 11-len_n)
    for r in range(1, rows):
        if r < rows - len_n:
            g[r][col] = 0
        else:
            g[r][col] = non_zeros[r - (rows - len_n)]

def apply_gravity_packing_special(g: List[List[int]]) -> None:
    # Compose: Apply special gravity packing to all columns
    if not g or not g[0]:
        return
    cols = len(g[0])
    for c in range(cols):
        pack_column_special(g, c)

def remove_other_large_groups_of_color(g: List[List[int]], c: int) -> None:
    # Observation: Remove all connected components (4-way) of color c with size >= 3, excluding the component containing top-left (0,0) to preserve isolated top-left cell
    if c == 0:
        return
    rows, cols = len(g), len(g[0])
    visited: Set[Tuple[int, int]] = set()
    # Mark the top-left component as visited without removing
    if g[0][0] == c:
        comp = find_connected_component(g, 0, 0)
        for p in comp:
            visited.add(p)
    # Scan for other components of c
    for r in range(rows):
        for cc in range(cols):
            pos = (r, cc)
            if pos not in visited and g[r][cc] == c:
                comp = find_connected_component(g, r, cc)
                if len(comp) >= 3:
                    remove_component_cells(g, comp)
                for p in comp:
                    visited.add(p)

def program(g: List[List[int]]) -> List[List[int]]:
    # Compose rules: Deep copy input, get top-left color c, remove other large groups of c, apply special gravity packing
    h = deepcopy(g)
    c = h[0][0]
    remove_other_large_groups_of_color(h, c)
    apply_gravity_packing_special(h)
    return h
```