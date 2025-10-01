```python
import collections
from typing import List
from copy import deepcopy

dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]

def flood_fill_component(g: List[List[int]], r: int, c: int, col: int, visited: List[List[bool]]) -> None:
    """Rule: Flood fill 4-way connected cells >4 with the given color, marking visited."""
    h, w = len(g), len(g[0])
    q = collections.deque([(r, c)])
    visited[r][c] = True
    g[r][c] = col
    while q:
        x, y = q.popleft()
        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            if 0 <= nx < h and 0 <= ny < w and g[nx][ny] > 4 and not visited[nx][ny]:
                visited[nx][ny] = True
                g[nx][ny] = col
                q.append((nx, ny))

def select_color(component_index: int) -> int:
    """Rule: Cycle through colors [4,3,1,2] based on component discovery order (0-based index)."""
    cycle = [4, 3, 1, 2]
    return cycle[component_index % len(cycle)]

def discover_and_color_above_4(g: List[List[int]]) -> List[List[int]]:
    """Rule: Scan row-major order, discover unvisited >4 cells, assign cycled color, flood fill."""
    h = len(g)
    if h == 0:
        return g
    w = len(g[0])
    visited = [[False] * w for _ in range(h)]
    component_index = 0
    for r in range(h):
        for c in range(w):
            if g[r][c] > 4 and not visited[r][c]:
                col = select_color(component_index)
                flood_fill_component(g, r, c, col, visited)
                component_index += 1
    return g

def preserve_cells_le_4(g: List[List[int]]) -> List[List[int]]:
    """Rule: Do not alter cells with values <=4 (including 0 and pre-colored 1-4)."""
    # This is handled implicitly by discovery_and_color_above_4, as it only targets >4.
    return g

def program(g: List[List[int]]) -> List[List[int]]:
    """Compose rules: Copy input, preserve <=4, discover and color >4 components."""
    g_copy = deepcopy(g)
    g_copy = preserve_cells_le_4(g_copy)
    g_copy = discover_and_color_above_4(g_copy)
    return g_copy
```