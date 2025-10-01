```python
from collections import deque
from typing import List, Tuple, Set

def find_start_position(grid: List[List[int]]) -> Tuple[int, int]:
    """Find the position of the pink 6, the starting point. Helpful for locating seed accurately."""
    h = len(grid)
    w = len(grid[0]) if h > 0 else 0
    for r in range(h):
        for c in range(w):
            if grid[r][c] == 6:
                return r, c
    return -1, -1

def find_connected_component(grid: List[List[int]], start_r: int, start_c: int) -> Set[Tuple[int, int]]:
    """Find the 4-connected component of non-1 cells (8 or 6) containing the start position using BFS. This identifies the region associated with the seed."""
    h = len(grid)
    w = len(grid[0]) if h > 0 else 0
    component: Set[Tuple[int, int]] = set()
    visited = [[False] * w for _ in range(h)]
    queue = deque([(start_r, start_c)])
    visited[start_r][start_c] = True
    component.add((start_r, start_c))
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while queue:
        r, c = queue.popleft()
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < h and 0 <= nc < w and not visited[nr][nc] and grid[nr][nc] != 1:
                visited[nr][nc] = True
                queue.append((nr, nc))
                component.add((nr, nc))
    return component

def is_boundary(grid: List[List[int]], r: int, c: int, h: int, w: int, component: Set[Tuple[int, int]]) -> bool:
    """Determine if a cell in the component is on its boundary: checks 8-directional neighbors for out-of-bounds, 1 (barrier), or non-1 cells outside the component. This rule identifies perimeter cells to fill."""
    dirs = [(dr, dc) for dr in [-1, 0, 1] for dc in [-1, 0, 1] if not (dr == 0 and dc == 0)]
    for dr, dc in dirs:
        nr = r + dr
        nc = c + dc
        if not (0 <= nr < h and 0 <= nc < w):
            return True
        if grid[nr][nc] == 1 or (grid[nr][nc] != 1 and (nr, nc) not in component):
            return True
    return False

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program: copies the grid, finds the component containing 6, and fills 8s on the boundary of that component with 7s, leaving interior 8s and the 6 unchanged. Composes component finding and boundary checking rules."""
    output = [row[:] for row in g]
    h = len(g)
    if h == 0:
        return output
    w = len(g[0])
    start_r, start_c = find_start_position(g)
    if start_r == -1:
        return output
    component = find_connected_component(g, start_r, start_c)
    for r, c in component:
        if g[r][c] == 8 and is_boundary(g, r, c, h, w, component):
            output[r][c] = 7
    return output
```