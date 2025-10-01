```python
from collections import deque
from typing import List, Tuple

def find_start_position(grid: List[List[int]]) -> Tuple[int, int]:
    """Find the position of the pink 6, the starting point for filling."""
    h = len(grid)
    w = len(grid[0]) if h > 0 else 0
    for r in range(h):
        for c in range(w):
            if grid[r][c] == 6:
                return r, c
    return -1, -1

def get_initial_fill_positions(grid: List[List[int]], start_r: int, start_c: int) -> list:
    """Get initial positions adjacent to 6 that are 8 (maroon) to start filling with 7 (dark red)."""
    h = len(grid)
    w = len(grid[0]) if h > 0 else 0
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    initial = []
    for dr, dc in directions:
        nr, nc = start_r + dr, start_c + dc
        if 0 <= nr < h and 0 <= nc < w and grid[nr][nc] == 8:
            initial.append((nr, nc))
    return initial

def perform_flood_fill(grid: List[List[int]], initial_positions: list):
    """Propagate the fill from initial positions, changing 8 to 7, blocking at 1 and 6."""
    h = len(grid)
    w = len(grid[0]) if h > 0 else 0
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    visited = [[False] * w for _ in range(h)]
    queue = deque()
    for r, c in initial_positions:
        grid[r][c] = 7
        visited[r][c] = True
        queue.append((r, c))
    while queue:
        r, c = queue.popleft()
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < h and 0 <= nc < w and grid[nr][nc] == 8 and not visited[nr][nc]:
                grid[nr][nc] = 7
                visited[nr][nc] = True
                queue.append((nr, nc))

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program: copy grid and perform flood fill from 6 to change connected 8's to 7's."""
    grid = [row[:] for row in g]
    start_r, start_c = find_start_position(grid)
    if start_r != -1:
        initial = get_initial_fill_positions(grid, start_r, start_c)
        perform_flood_fill(grid, initial)
    return grid
```