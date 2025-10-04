```python
from collections import deque
from typing import List, Set, Tuple

def get_border_eights(g: List[List[int]]) -> List[Tuple[int, int]]:
    """Collect all positions on the grid border that contain 8."""
    n = len(g)
    borders: List[Tuple[int, int]] = []
    # Top and bottom rows
    for c in range(n):
        if g[0][c] == 8:
            borders.append((0, c))
        if g[n - 1][c] == 8:
            borders.append((n - 1, c))
    # Left and right columns, excluding corners
    for r in range(1, n - 1):
        if g[r][0] == 8:
            borders.append((r, 0))
        if g[r][n - 1] == 8:
            borders.append((r, n - 1))
    return borders

def flood_reachable_8s(starts: List[Tuple[int, int]], g: List[List[int]]) -> Set[Tuple[int, int]]:
    """Perform BFS flood fill from starting border 8 positions through adjacent 8 cells (4-directional)."""
    if not starts:
        return set()
    n = len(g)
    visited: Set[Tuple[int, int]] = set(starts)
    queue = deque(starts)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while queue:
        r, c = queue.popleft()
        for dr, dc in directions:
            nr = r + dr
            nc = c + dc
            if 0 <= nr < n and 0 <= nc < n and g[nr][nc] == 8 and (nr, nc) not in visited:
                visited.add((nr, nc))
                queue.append((nr, nc))
    return visited

def fill_enclosed_regions(g: List[List[int]], reachable: Set[Tuple[int, int]]) -> List[List[int]]:
    """Copy the input grid and change unreachable 8 cells to 2, preserving all other cells."""
    n = len(g)
    output = [row[:] for row in g]
    for r in range(n):
        for c in range(n):
            if output[r][c] == 8 and (r, c) not in reachable:
                output[r][c] = 2
    return output

def program(g: List[List[int]]) -> List[List[int]]:
    """Solve the puzzle by filling enclosed 8 regions (unreachable from borders) with 2."""
    starts = get_border_eights(g)
    reachable = flood_reachable_8s(starts, g)
    return fill_enclosed_regions(g, reachable)
```