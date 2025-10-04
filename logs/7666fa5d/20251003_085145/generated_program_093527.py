```python
from typing import List, Tuple
from collections import deque

def is_border(r: int, c: int, n: int) -> bool:
    return r == 0 or r == n - 1 or c == 0 or c == n - 1

def get_neighbors(r: int, c: int, n: int) -> List[Tuple[int, int]]:
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    return [(r + dr, c + dc) for dr, dc in dirs if 0 <= r + dr < n and 0 <= c + dc < n]

def flood_from_border(g: List[List[int]]) -> set:
    n = len(g)
    visited = set()
    queue = deque()
    for r in range(n):
        for c in range(n):
            if is_border(r, c, n) and g[r][c] == 8:
                queue.append((r, c))
                visited.add((r, c))
    while queue:
        cr, cc = queue.popleft()
        for nr, nc in get_neighbors(cr, cc, n):
            if g[nr][nc] == 8 and (nr, nc) not in visited:
                visited.add((nr, nc))
                queue.append((nr, nc))
    return visited

def fill_enclosed(g: List[List[int]], visited: set) -> List[List[int]]:
    n = len(g)
    new_grid = [row[:] for row in g]
    for r in range(n):
        for c in range(n):
            if new_grid[r][c] == 8 and (r, c) not in visited:
                new_grid[r][c] = 2
    return new_grid

def program(g: List[List[int]]) -> List[List[int]]:
    visited = flood_from_border(g)
    return fill_enclosed(g, visited)
```