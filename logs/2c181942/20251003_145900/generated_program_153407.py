```python
from typing import List
from collections import Counter

def count_main_colors(g: List[List[int]]) -> dict:
    # observation: conserve pixels of 1,2,3
    flat = [cell for row in g for cell in row]
    c = Counter(flat)
    return {k: c[k] for k in [1,2,3] if k in c}

def create_background_grid(h: int, w: int) -> List[List[int]]:
    # rule: background is 8, other colors erased unless main
    return [[8] * w for _ in range(h)]

def place_color_bar(grid: List[List[int]], color: int, num: int, start_col: int, center_row: int) -> None:
    # rule: place as vertical bar centered vertically, adjacent to center
    start_row = center_row - (num // 2)
    for i in range(num):
        row = start_row + i
        if 0 <= row < len(grid):
            grid[row][start_col] = color

def program(g: List[List[int]]) -> List[List[int]]:
    h = len(g)
    w = len(g[0]) if h > 0 else 0
    counts = count_main_colors(g)
    new_grid = create_background_grid(h, w)
    center_row = h // 2
    center_col = w // 2
    positions = [-1, 0, 1]  # relative cols
    color_order = [3, 1, 2]  # left green, mid blue, right red
    for idx, c in enumerate(color_order):
        if c in counts:
            col = center_col + positions[idx]
            if 0 <= col < w:
                place_color_bar(new_grid, c, counts[c], col, center_row)
    return new_grid
```