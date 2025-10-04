```python
from typing import List

def get_colors(g: List[List[int]]) -> set:
    colors = set()
    for row in g:
        for val in row:
            colors.add(val)
    return colors

def background_color(g: List[List[int]]) -> int:
    colors = get_colors(g)
    if len(colors) == 0:
        return 0
    # Assume smallest is background
    return min(colors)

def create_empty_grid(size: int, bg: int) -> List[List[int]]:
    return [[bg for _ in range(size)] for _ in range(size)]

def place_input_in_top_left(grid: List[List[int]], g: List[List[int]]) -> List[List[int]]:
    h = len(g)
    w = len(g[0]) if h > 0 else 0
    for i in range(h):
        for j in range(w):
            grid[i][j] = g[i][j]
    return grid

def tile_remaining_columns(grid: List[List[int]], g: List[List[int]]) -> List[List[int]]:
    h_in = len(g)
    w_in = len(g[0]) if h_in > 0 else 0
    size = 20
    for i in range(size):
        in_row = i % h_in
        for j in range(w_in, size):
            grid[i][j] = g[in_row][(j - w_in) % w_in]
    return grid

def extend_bottom_rows(grid: List[List[int]], g: List[List[int]]) -> List[List[int]]:
    h_in = len(g)
    w_in = len(g[0]) if h_in > 0 else 0
    size = 20
    for i in range(h_in, size):
        in_row = (i - h_in) % h_in
        for j in range(size):
            if j < w_in:
                grid[i][j] = g[in_row][j]
            else:
                grid[i][j] = g[in_row][(j - w_in) % w_in]
    return grid

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        bg = 0
    else:
        bg = background_color(g)
    grid = create_empty_grid(20, bg)
    grid = place_input_in_top_left(grid, g)
    grid = tile_remaining_columns(grid, g)
    grid = extend_bottom_rows(grid, g)
    return grid
```