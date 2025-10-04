```python
from typing import List, Tuple
from collections import Counter

directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def mode_ignoring_noise(lst: List[int]) -> int:
    counts = Counter(x for x in lst if x not in (0, 1))
    if not counts:
        return 0
    return counts.most_common(1)[0][0]

def find_horizontal_stripes(grid: List[List[int]]) -> List[Tuple[int, int, int]]:
    if not grid:
        return []
    n_rows = len(grid)
    n_cols = len(grid[0])
    stripes = []
    i = 0
    while i < n_rows:
        row_mode = mode_ignoring_noise(grid[i])
        start = i
        i += 1
        while i < n_rows:
            next_mode = mode_ignoring_noise(grid[i])
            if next_mode != row_mode:
                break
            i += 1
        height = i - start
        stripes.append((start, height, row_mode))
    return stripes

def subdivide_stripe_horizontally(grid: List[List[int]], start_row: int, end_row: int) -> List[Tuple[int, int, int]]:
    if not grid or not grid[0]:
        return []
    n_cols = len(grid[0])
    subblocks = []
    j = 0
    while j < n_cols:
        col_segment = [grid[k][j] for k in range(start_row, end_row)]
        col_mode = mode_ignoring_noise(col_segment)
        start = j
        j += 1
        while j < n_cols:
            next_segment = [grid[k][j] for k in range(start_row, end_row)]
            next_mode = mode_ignoring_noise(next_segment)
            if next_mode != col_mode:
                break
            j += 1
        width = j - start
        subblocks.append((start, width, col_mode))
    return subblocks

def map_mode(m: int) -> int:
    if m == 6:
        return 7
    if m == 4:
        return 0
    if m == 8:
        return 0
    if m == 9:
        return 3
    if m == 5:
        return 9
    return m

def build_blocky_grid(grid: List[List[int]], stripes: List[Tuple[int, int, int]]) -> List[List[int]]:
    h = len(grid)
    w = len(grid[0]) if grid else 0
    new_grid = [[0] * w for _ in range(h)]
    for start_row, height, row_mode in stripes:
        subblocks = subdivide_stripe_horizontally(grid, start_row, start_row + height)
        mapped_row_mode = map_mode(row_mode)
        for start_col, width, col_mode in subblocks:
            color = map_mode(col_mode) if col_mode != 0 else mapped_row_mode
            for ii in range(start_row, start_row + height):
                for jj in range(start_col, start_col + width):
                    new_grid[ii][jj] = color
    return new_grid

def expand_three_into_zeros(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return g
    r, c = len(g), len(g[0])
    changed = True
    while changed:
        changed = False
        new_g = [row[:] for row in g]
        for i in range(r):
            for j in range(c):
                if g[i][j] == 0:
                    adjacent_three = any(
                        0 <= i + di < r and 0 <= j + dj < c and g[i + di][j + dj] == 3
                        for di, dj in directions
                    )
                    if adjacent_three:
                        new_g[i][j] = 3
                        changed = True
        g = new_g
    return g

def transpose(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return []
    return [list(row) for row in zip(*g)]

def program(g: List[List[int]]) -> List[List[int]]:
    stripes = find_horizontal_stripes(g)
    g = build_blocky_grid(g, stripes)
    g = expand_three_into_zeros(g)
    g = transpose(g)
    return g
```