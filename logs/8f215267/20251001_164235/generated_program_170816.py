```python
from collections import deque
from typing import List, Tuple

def get_background(g: List[List[int]]) -> int:
    """Identify the background color from the top-left border cell."""
    return g[0][0]

def clean_small_components(g: List[List[int]], bg: int, max_size: int = 5) -> List[List[int]]:
    """Remove small connected components (size <= max_size) of non-background colors by replacing them with background.
    Uses 4-directional connectivity for same color."""
    rows = len(g)
    cols = len(g[0])
    visited = [[False] * cols for _ in range(rows)]
    new_g = [row[:] for row in g]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for r in range(rows):
        for c in range(cols):
            if g[r][c] == bg or visited[r][c]:
                continue
            component_color = g[r][c]
            queue = deque([(r, c)])
            visited[r][c] = True
            size = 1
            component = [(r, c)]
            while queue:
                cr, cc = queue.popleft()
                for dr, dc in directions:
                    nr = cr + dr
                    nc = cc + dc
                    if 0 <= nr < rows and 0 <= nc < cols and not visited[nr][nc] and g[nr][nc] == component_color:
                        visited[nr][nc] = True
                        queue.append((nr, nc))
                        size += 1
                        component.append((nr, nc))
            if size <= max_size:
                for pr, pc in component:
                    new_g[pr][pc] = bg
    return new_g

def has_non_bg_after(g: List[List[int]], after_row: int, bg: int) -> bool:
    """Check if there is any non-background cell after the given row."""
    rows = len(g)
    cols = len(g[0])
    for r in range(after_row, rows):
        for j in range(cols):
            if g[r][j] != bg:
                return True
    return False

def find_connected_components(g: List[List[int]], bg: int) -> List[Tuple[int, int, int, int, int]]:
    """Find all connected components of non-bg colors (4-dir, same color), return list of (color, min_r, max_r, min_c, max_c) for large ones (h>=5, w>=3)."""
    rows = len(g)
    cols = len(g[0])
    visited = [[False] * cols for _ in range(rows)]
    components = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for r in range(rows):
        for c in range(cols):
            if g[r][c] == bg or visited[r][c]:
                continue
            color = g[r][c]
            queue = deque([(r, c)])
            visited[r][c] = True
            min_r, max_r = r, r
            min_c, max_c = c, c
            size = 1
            while queue:
                cr, cc = queue.popleft()
                min_r = min(min_r, cr)
                max_r = max(max_r, cr)
                min_c = min(min_c, cc)
                max_c = max(max_c, cc)
                for dr, dc in directions:
                    nr = cr + dr
                    nc = cc + dc
                    if 0 <= nr < rows and 0 <= nc < cols and not visited[nr][nc] and g[nr][nc] == color:
                        visited[nr][nc] = True
                        queue.append((nr, nc))
                        size += 1
            h = max_r - min_r + 1
            w = max_c - min_c + 1
            if h >= 5 and w >= 3 and size > 5:
                components.append((color, min_r, max_r, min_c, max_c))
    return components

def compute_bounds(g: List[List[int]], c: int, min_r: int, max_r: int, min_c: int, max_c: int) -> Tuple[int, int, int, int]:
    """Compute side_L, side_R from middle rows, overall_L, overall_R from bounding box."""
    overall_L = min_c
    overall_R = max_c
    middle_min_r = min_r + 1
    middle_max_r = max_r - 1
    row_min_list = []
    row_max_list = []
    cols = len(g[0])
    for r in range(middle_min_r, middle_max_r + 1):
        row_cols = [j for j in range(min_c, min(max_c + 1, cols)) if g[r][j] == c]
        if row_cols:
            row_min_list.append(min(row_cols))
            row_max_list.append(max(row_cols))
    if row_min_list:
        side_L = max(row_min_list)
        side_R = min(row_max_list)
    else:
        side_L = overall_L
        side_R = overall_R
    return side_L, side_R, overall_L, overall_R

def process_component(g: List[List[int]], c: int, min_r: int, max_r: int, min_c: int, max_c: int, bg: int) -> List[List[int]]:
    """Process a single component into a frame with pattern using computed bounds."""
    side_L, side_R, overall_L, overall_R = compute_bounds(g, c, min_r, max_r, min_c, max_c)
    cols = len(g[0])
    # Set full top
    for j in range(overall_L, overall_R + 1):
        if j < cols:
            g[min_r][j] = c
    # Set full bottom
    for j in range(overall_L, overall_R + 1):
        if j < cols:
            g[max_r][j] = c
    # Set sides and interior for middle rows
    for r in range(min_r + 1, max_r):
        if side_L < cols:
            g[r][side_L] = c
        if side_R < cols:
            g[r][side_R] = c
        for j in range(side_L + 1, side_R):
            g[r][j] = bg
    # Pattern in middle row
    middle = min_r + 2
    if min_r + 1 <= middle <= max_r - 1:
        k = (c + 1) // 2
        for i in range(1, k + 1):
            col = side_R - 2 * i
            if side_L < col < side_R and 0 <= col < cols:
                g[middle][col] = c
    return g

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program: clean noise, find large components, process each into frame."""
    bg = get_background(g)
    g = clean_small_components(g, bg, max_size=5)
    components = find_connected_components(g, bg)
    components.sort(key=lambda comp: comp[1])  # Sort by min_r
    for comp in components:
        c, min_r, max_r, min_c, max_c = comp
        g = process_component(g, c, min_r, max_r, min_c, max_c, bg)
    return g
```