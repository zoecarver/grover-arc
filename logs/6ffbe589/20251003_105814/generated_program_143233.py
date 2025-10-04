```python
from typing import List, Tuple

def count_nonzeros(row: List[int]) -> int:
    """Count non-zero elements in a row."""
    return sum(1 for x in row if x != 0)

def row_counts(g: List[List[int]]) -> List[int]:
    """Compute non-zero counts for each row in the grid."""
    return [count_nonzeros(row) for row in g]

def max_contiguous_sum_indices(counts: List[int]) -> Tuple[int, int]:
    """Find start and end indices of the contiguous row block with maximum sum of non-zero counts using Kadane's algorithm."""
    n = len(counts)
    if n == 0:
        return 0, -1
    max_current = max_global = counts[0]
    current_start = global_start = 0
    global_end = 0
    for i in range(1, n):
        if counts[i] > max_current + counts[i]:
            max_current = counts[i]
            current_start = i
        else:
            max_current += counts[i]
        if max_current > max_global:
            max_global = max_current
            global_start = current_start
            global_end = i
    return global_start, global_end

def compute_first_last(g: List[List[int]]) -> Tuple[List[int], List[int]]:
    """Compute first and last non-zero column indices for each row."""
    if not g:
        return [], []
    n_cols = len(g[0])
    firsts = [n_cols] * len(g)
    lasts = [-1] * len(g)
    for i, row in enumerate(g):
        for j, val in enumerate(row):
            if val != 0:
                firsts[i] = min(firsts[i], j)
                lasts[i] = max(lasts[i], j)
    return firsts, lasts

def get_col_bounds(firsts: List[int], lasts: List[int], start: int, end: int, n_cols: int) -> Tuple[int, int]:
    """Compute global min first and max last non-zero columns over the row block."""
    block_firsts = [firsts[k] for k in range(start, end + 1) if firsts[k] < n_cols]
    block_lasts = [lasts[k] for k in range(start, end + 1) if lasts[k] >= 0]
    if not block_firsts:
        return 0, 0
    return min(block_firsts), max(block_lasts)

def crop_grid(g: List[List[int]], row_start: int, row_end: int, col_start: int, col_end: int) -> List[List[int]]:
    """Crop the grid to the specified row and column range."""
    return [row[col_start:col_end + 1] for row in g[row_start:row_end + 1]]

def pad_dimension(grid: List[List[int]], target: int, is_row: bool) -> List[List[int]]:
    """Pad rows or columns of the grid to the target size, centered with zeros."""
    if not grid:
        return grid
    current = len(grid) if is_row else len(grid[0])
    if current >= target:
        return grid
    pad_total = target - current
    pad_before = pad_total // 2
    pad_after = pad_total - pad_before
    if is_row:
        zero_row = [0] * len(grid[0])
        grid = [zero_row[:] for _ in range(pad_before)] + grid + [zero_row[:] for _ in range(pad_after)]
    else:
        for i in range(len(grid)):
            grid[i] = [0] * pad_before + grid[i] + [0] * pad_after
    return grid

def pad_to_square(grid: List[List[int]]) -> List[List[int]]:
    """Pad the cropped grid to a square by centering content in both dimensions."""
    if not grid:
        return [[0]]
    h = len(grid)
    w = len(grid[0]) if h > 0 else 0
    s = max(h, w) if h > 0 and w > 0 else 1
    grid = pad_dimension(grid, s, False)  # Pad columns first
    grid = pad_dimension(grid, s, True)   # Pad rows second
    return grid

def program(g: List[List[int]]) -> List[List[int]]:
    """Main function: extract the main patterned object by selecting the densest contiguous row block, cropping to its column bounds, and padding to a square."""
    if not g or not g[0]:
        return [[0]]
    counts = row_counts(g)
    start, end = max_contiguous_sum_indices(counts)
    if end < start:
        return [[0]]
    firsts, lasts = compute_first_last(g)
    n_cols = len(g[0]) if g else 0
    min_c, max_c = get_col_bounds(firsts, lasts, start, end, n_cols)
    if min_c > max_c:
        return [[0]]
    cropped = crop_grid(g, start, end, min_c, max_c)
    return pad_to_square(cropped)
```