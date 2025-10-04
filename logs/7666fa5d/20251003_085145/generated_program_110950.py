```python
from typing import List, Tuple
from collections import deque
import copy

def find_boundary_color(grid: List[List[int]]) -> int:
    colors = set(cell for row in grid for cell in row if cell != 0)
    if len(colors) != 1:
        raise ValueError("Expected exactly one non-zero color")
    return next(iter(colors))

def is_border(i: int, j: int, n: int = 16) -> bool:
    return i == 0 or i == n - 1 or j == 0 or j == n - 1

def get_neighbors(i: int, j: int, n: int = 16) -> List[Tuple[int, int]]:
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    neighbors = []
    for di, dj in directions:
        ni, nj = i + di, j + dj
        if 0 <= ni < n and 0 <= nj < n:
            neighbors.append((ni, nj))
    return neighbors

def flood_outside_positions(grid: List[List[int]], boundary_color: int) -> set[Tuple[int, int]]:
    n = len(grid)
    visited: set[Tuple[int, int]] = set()
    q = deque()
    for i in range(n):
        # Enqueue border zeros
        if is_border(i, 0) and grid[i][0] == 0:
            pos = (i, 0)
            if pos not in visited:
                visited.add(pos)
                q.append(pos)
        if is_border(i, n - 1) and grid[i][n - 1] == 0:
            pos = (i, n - 1)
            if pos not in visited:
                visited.add(pos)
                q.append(pos)
    for j in range(1, n - 1):
        # Top and bottom borders, excluding corners already done
        if grid[0][j] == 0:
            pos = (0, j)
            if pos not in visited:
                visited.add(pos)
                q.append(pos)
        if grid[n - 1][j] == 0:
            pos = (n - 1, j)
            if pos not in visited:
                visited.add(pos)
                q.append(pos)
    while q:
        ci, cj = q.popleft()
        for ni, nj in get_neighbors(ci, cj):
            if grid[ni][nj] == 0 and (ni, nj) not in visited:
                visited.add((ni, nj))
                q.append((ni, nj))
    return visited

def fill_enclosed_regions(grid: List[List[int]], outside_positions: set[Tuple[int, int]]) -> List[List[int]]:
    n = len(grid)
    result = [row[:] for row in grid]
    for i in range(n):
        for j in range(n):
            if result[i][j] == 0 and (i, j) not in outside_positions:
                result[i][j] = 1
    return result

def program(g: List[List[int]]) -> List[List[int]]:
    boundary_color = find_boundary_color(g)
    outside = flood_outside_positions(g, boundary_color)
    return fill_enclosed_regions(g, outside)
```