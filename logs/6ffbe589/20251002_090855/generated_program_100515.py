```python
import math
from typing import List, Tuple

def get_eight_neighbors(r: int, c: int, n: int) -> List[Tuple[int, int]]:
    """
    Generates 8 possible neighboring positions within bounds for 8-connectivity.
    """
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    neighbors = []
    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        if 0 <= nr < n and 0 <= nc < n:
            neighbors.append((nr, nc))
    return neighbors

def find_all_components(g: List[List[int]]) -> List[List[Tuple[int, int]]]:
    """
    Uses DFS with stack to find all 8-connected components of non-zero cells.
    """
    n = len(g)
    visited = set()
    components = []
    for i in range(n):
        for j in range(n):
            if g[i][j] != 0 and (i, j) not in visited:
                component = []
                stack = [(i, j)]
                while stack:
                    cr, cc = stack.pop()
                    if (cr, cc) in visited:
                        continue
                    visited.add((cr, cc))
                    component.append((cr, cc))
                    for nr, nc in get_eight_neighbors(cr, cc, n):
                        if g[nr][nc] != 0 and (nr, nc) not in visited:
                            stack.append((nr, nc))
                components.append(component)
    return components

def get_bounding_box(component: List[Tuple[int, int]]) -> Tuple[int, int, int, int]:
    """
    Computes min/max row/col for a component's tight bounding box.
    """
    if not component:
        return 0, -1, 0, -1
    min_r = min(r for r, c in component)
    max_r = max(r for r, c in component)
    min_c = min(c for r, c in component)
    max_c = max(c for r, c in component)
    return min_r, max_r, min_c, max_c

def select_main_component(components: List[List[Tuple[int, int]]], n: int) -> List[Tuple[int, int]]:
    """
    Selects the main component: the one closest to grid center (n/2, n/2), ties broken by largest size.
    """
    if not components:
        return []
    min_dist = float('inf')
    best_comp = None
    best_size = 0
    for comp in components:
        min_r, max_r, min_c, max_c = get_bounding_box(comp)
        center_r = (min_r + max_r) / 2.0
        center_c = (min_c + max_c) / 2.0
        dist = math.sqrt((center_r - n / 2.0) ** 2 + (center_c - n / 2.0) ** 2)
        size = len(comp)
        if dist < min_dist or (dist == min_dist and size > best_size):
            min_dist = dist
            best_comp = comp
            best_size = size
    return best_comp

def extract_subgrid(g: List[List[int]], min_r: int, max_r: int, min_c: int, max_c: int) -> List[List[int]]:
    """
    Extracts the subgrid from the given bounding box.
    """
    return [row[min_c:max_c + 1] for row in g[min_r:max_r + 1]]

def pad_to_square(grid: List[List[int]]) -> List[List[int]]:
    """
    Pads the grid to a square of side max(height, width), centered with zeros.
    """
    if not grid:
        return []
    h = len(grid)
    w = len(grid[0]) if h > 0 else 0
    n = max(h, w)
    pad_top = (n - h) // 2
    pad_bottom = n - h - pad_top
    pad_left = (n - w) // 2
    pad_right = n - w - pad_left
    padded = [[0] * n for _ in range(n)]
    for i in range(h):
        for j in range(w):
            padded[pad_top + i][pad_left + j] = grid[i][j]
    return padded

def program(g: List[List[int]]) -> List[List[int]]:
    """
    Main program: finds central largest connected component, extracts its bounding subgrid, pads to square.
    """
    n = len(g)
    components = find_all_components(g)
    main_comp = select_main_component(components, n)
    if not main_comp:
        return [[0] * n for _ in range(n)]
    min_r, max_r, min_c, max_c = get_bounding_box(main_comp)
    sub = extract_subgrid(g, min_r, max_r, min_c, max_c)
    return pad_to_square(sub)
```