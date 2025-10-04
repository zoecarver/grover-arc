```python
from typing import List, Tuple
from copy import deepcopy

def find_max_color(grid: List[List[int]]) -> int:
    if not grid or not grid[0]:
        return 0
    return max((max(row) for row in grid), default=0)

def get_appearance_palette(grid: List[List[int]]) -> List[int]:
    max_c = find_max_color(grid)
    seen = set()
    palette = []
    for row in grid:
        for c in row:
            if 0 < c < max_c and c not in seen:
                seen.add(c)
                palette.append(c)
    return palette

def get_high_components(grid: List[List[int]]) -> List[List[Tuple[int, int]]]:
    size = len(grid)
    visited = [[False] * size for _ in range(size)]
    components = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(size):
        for j in range(size):
            if grid[i][j] > 4 and not visited[i][j]:
                positions = []
                stack = [(i, j)]
                visited[i][j] = True
                while stack:
                    x, y = stack.pop()
                    positions.append((x, y))
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < size and 0 <= ny < size and grid[nx][ny] > 4 and not visited[nx][ny]:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                components.append(positions)
    return components

def fill_bounding_box(grid: List[List[int]], positions: List[Tuple[int, int]], color: int) -> List[List[int]]:
    if not positions:
        return grid
    min_i = min(p[0] for p in positions)
    max_i = max(p[0] for p in positions)
    min_j = min(p[1] for p in positions)
    max_j = max(p[1] for p in positions)
    new_grid = [row[:] for row in grid]
    for i in range(min_i, max_i + 1):
        for j in range(min_j, max_j + 1):
            new_grid[i][j] = color
    return new_grid

def program(g: List[List[int]]) -> List[List[int]]:
    h = [row[:] for row in g]
    palette = get_appearance_palette(g)
    if not palette:
        return h
    components = get_high_components(g)
    for cid, positions in enumerate(components):
        color = palette[cid % len(palette)]
        h = fill_bounding_box(h, positions, color)
    return h
```