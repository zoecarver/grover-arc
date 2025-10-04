```python
from collections import deque
from typing import List, Tuple

def find_six(grid: List[List[int]]) -> Tuple[int, int]:
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == 6:
                return r, c
    raise ValueError("No 6 found")

def get_component(grid: List[List[int]], start_r: int, start_c: int) -> set:
    rows = len(grid)
    cols = len(grid[0])
    component = set()
    q = deque()
    q.append((start_r, start_c))
    component.add((start_r, start_c))
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while q:
        r, c = q.popleft()
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in component and grid[nr][nc] == 8:
                component.add((nr, nc))
                q.append((nr, nc))
    return component

def is_boundary(r: int, c: int, component: set, rows: int, cols: int) -> bool:
    directions8 = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for dr, dc in directions8:
        nr, nc = r + dr, c + dc
        if not (0 <= nr < rows and 0 <= nc < cols):
            return True
        if (nr, nc) not in component:
            return True
    return False

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return []
    rows, cols = len(g), len(g[0])
    start_r, start_c = find_six(g)
    component = get_component(g, start_r, start_c)
    output = [row[:] for row in g]
    for r, c in component:
        if g[r][c] == 8 and is_boundary(r, c, component, rows, cols):
            output[r][c] = 7
    return output
```