```python
from typing import List, Tuple

def find_bbox(g: List[List[int]], color: int, N: int) -> Tuple[int, int, int, int]:
    """Find the bounding box (min_r, max_r, min_c, max_c) of cells with the given color."""
    min_r = N
    max_r = -1
    min_c = N
    max_c = -1
    for r in range(N):
        for c in range(N):
            if g[r][c] == color:
                min_r = min(min_r, r)
                max_r = max(max_r, r)
                min_c = min(min_c, c)
                max_c = max(max_c, c)
    return min_r, max_r, min_c, max_c

def get_base_width(g: List[List[int]], N: int, row: int, min_c: int, max_c: int) -> int:
    """Compute the width of the consecutive 1's run in the given row covering min_c to max_c."""
    left = min_c
    while left > 0 and g[row][left - 1] == 1:
        left -= 1
    right = max_c
    while right < N - 1 and g[row][right + 1] == 1:
        right += 1
    return right - left + 1

def is_merge_condition(g: List[List[int]], N: int, red_min_r: int, red_max_r: int, red_min_c: int, red_max_c: int, h: int, w: int) -> bool:
    """Determine if the red shape should be merged based on attachment base width equaling red width when touching top or bottom."""
    if red_min_r == 0:
        attach_row = red_max_r + 1
        if attach_row < N:
            base_width = get_base_width(g, N, attach_row, red_min_c, red_max_c)
            return base_width == w
    if red_max_r == N - 1:
        attach_row = red_min_r - 1
        if attach_row >= 0:
            base_width = get_base_width(g, N, attach_row, red_min_c, red_max_c)
            return base_width == w
    return False

def apply_fill(new_grid: List[List[int]], zero_min_r: int, zero_max_r: int, zero_min_c: int, zero_max_c: int, h: int, w: int, N: int):
    """Fill the bottom h x w sub-rectangle of the zero bounding box with 1's (assumes sufficient size)."""
    fill_min_r = max(zero_min_r, zero_max_r - h + 1)
    fill_min_c = zero_min_c
    fill_max_c = min(zero_max_c, zero_min_c + w - 1)
    for r in range(fill_min_r, zero_max_r + 1):
        for c in range(fill_min_c, fill_max_c + 1):
            new_grid[r][c] = 1

def apply_merge(new_grid: List[List[int]], red_min_r: int, red_max_r: int, red_min_c: int, red_max_c: int):
    """Turn the red rectangle to 0's for merge case."""
    for r in range(red_min_r, red_max_r + 1):
        for c in range(red_min_c, red_max_c + 1):
            new_grid[r][c] = 0

def apply_split_cut(new_grid: List[List[int]], N: int, red_min_c: int, red_max_r: int, h: int, w: int):
    """Apply the split cut by turning a computed h x w rectangle of 1's to 0's."""
    delta = N // 2 - (1 if red_min_c == 0 else 0)
    col_start = red_min_c + delta
    if col_start + w > N:
        col_start = N // 2 - w // 2 + 1
    row_start = N // 2 if red_max_r == N - 1 else (N // 2 - h + 1)
    for r in range(row_start, row_start + h):
        for c in range(col_start, col_start + w):
            if 0 <= r < N and 0 <= c < N:
                new_grid[r][c] = 0

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program: infer rules from examples to transform the grid based on red-blue interactions."""
    N = len(g)
    if N == 0:
        return g
    new_grid = [row[:] for row in g]
    red_bbox = find_bbox(g, 2, N)
    if red_bbox[1] == -1:  # no red
        return new_grid
    red_min_r, red_max_r, red_min_c, red_max_c = red_bbox
    h = red_max_r - red_min_r + 1
    w = red_max_c - red_min_c + 1
    zero_bbox = find_bbox(g, 0, N)
    if zero_bbox[1] == -1:  # no zeros
        return new_grid
    zero_min_r, zero_max_r, zero_min_c, zero_max_c = zero_bbox
    # Apply fill (common to merge and split)
    apply_fill(new_grid, zero_min_r, zero_max_r, zero_min_c, zero_max_c, h, w, N)
    # Determine and apply transformation
    if is_merge_condition(g, N, red_min_r, red_max_r, red_min_c, red_max_c, h, w):
        apply_merge(new_grid, red_min_r, red_max_r, red_min_c, red_max_c)
    else:
        apply_split_cut(new_grid, N, red_min_c, red_max_r, h, w)
    return new_grid
```