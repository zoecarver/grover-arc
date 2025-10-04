```python
from typing import List
from collections import deque

def find_special_color(grid: List[List[int]]) -> int:
    for row in grid:
        for cell in row:
            if cell != 8:
                return cell
    return None

def get_border_eights_positions(n: int, grid: List[List[int]]) -> list:
    positions = []
    for i in range(n):
        if grid[0][i] == 8:
            positions.append((0, i))
        if grid[n-1][i] == 8:
            positions.append((n-1, i))
        if grid[i][0] == 8:
            positions.append((i, 0))
        if grid[i][n-1] == 8:
            positions.append((i, n-1))
    return positions

def flood_fill_outside(n: int, start_positions: list, grid: List[List[int]]) -> set:
    outside = set()
    q = deque(start_positions)
    for pos in start_positions:
        outside.add(pos)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while q:
        x, y = q.popleft()
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < n and grid[nx][ny] == 8 and (nx, ny) not in outside:
                outside.add((nx, ny))
                q.append((nx, ny))
    return outside

def fill_enclosed_regions(grid: List[List[int]], outside: set, fill_color: int = 2) -> List[List[int]]:
    n = len(grid)
    result = [row[:] for row in grid]
    for i in range(n):
        for j in range(n):
            if result[i][j] == 8 and (i, j) not in outside:
                result[i][j] = fill_color
    return result

def program(g: List[List[int]]) -> List[List[int]]:
    grid_copy = [row[:] for row in g]
    n = len(grid_copy)
    special_color = find_special_color(grid_copy)
    if special_color is None:
        return grid_copy
    border_positions = get_border_eights_positions(n, grid_copy)
    outside_positions = flood_fill_outside(n, border_positions, grid_copy)
    return fill_enclosed_regions(grid_copy, outside_positions)
```