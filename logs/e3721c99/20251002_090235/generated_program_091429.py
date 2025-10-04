```python
from typing import List

def find_max_color(grid: List[List[int]]) -> int:
    return max((max(row) for row in grid), default=0)

def find_palette(grid: List[List[int]]) -> List[int]:
    max_c = find_max_color(grid)
    seen = set()
    palette = []
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            c = grid[i][j]
            if 0 < c < max_c and c not in seen:
                seen.add(c)
                palette.append(c)
    return palette

def has_full_one_row(grid: List[List[int]]) -> bool:
    size = len(grid)
    for row in grid:
        if all(c == 1 for c in row):
            return True
    return False

def get_palette(grid: List[List[int]]) -> List[int]:
    palette = find_palette(grid)
    if not has_full_one_row(grid):
        palette = [c for c in palette if c != 1]
    return palette

def compute_replacement(i: int, j: int, palette: List[int]) -> int:
    if not palette:
        return 0
    return palette[(i + j) % len(palette)]

def replace_high_colors(grid: List[List[int]]) -> List[List[int]]:
    palette = get_palette(grid)
    max_c = find_max_color(grid)
    size = len(grid)
    new_grid = [row[:] for row in grid]
    for i in range(size):
        for j in range(size):
            if new_grid[i][j] == max_c:
                new_grid[i][j] = compute_replacement(i, j, palette)
    return new_grid

def program(g: List[List[int]]) -> List[List[int]]:
    return replace_high_colors(g)
```