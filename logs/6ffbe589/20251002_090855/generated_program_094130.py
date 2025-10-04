```python
import typing as tp

def is_non_empty_row(row: tp.List[int]) -> bool:
    """Rule: Check if a row contains any non-zero value."""
    return any(x != 0 for x in row)

def find_longest_consecutive_non_empty_rows(g: tp.List[tp.List[int]]) -> tp.Tuple[int, int]:
    """Observation: Identify the longest sequence of consecutive non-empty rows in the grid."""
    n = len(g)
    max_length = 0
    best_start = 0
    best_end = 0
    start = 0
    for i in range(n):
        if is_non_empty_row(g[i]):
            continue
        length = i - start
        if length > max_length:
            max_length = length
            best_start = start
            best_end = i - 1
        start = i
    length = n - start
    if length > max_length:
        max_length = length
        best_start = start
        best_end = n - 1
    return best_start, best_end

def find_bounding_columns(g: tp.List[tp.List[int]], min_r: int, max_r: int) -> tp.Tuple[int, int]:
    """Rule: Compute the minimum and maximum column indices with non-zero values in the main row block."""
    m = len(g[0])
    min_c = m
    max_c = -1
    for r in range(min_r, max_r + 1):
        for c in range(m):
            if g[r][c] != 0:
                min_c = min(min_c, c)
                max_c = max(max_c, c)
    return min_c, max_c

def crop_to_bounding_box(g: tp.List[tp.List[int]], min_r: int, max_r: int, min_c: int, max_c: int) -> tp.List[tp.List[int]]:
    """Transformation: Extract the subgrid from the bounding box of the main block."""
    return [[g[r][c] for c in range(min_c, max_c + 1)] for r in range(min_r, max_r + 1)]

def compute_target_size(row_span: int, col_span: int) -> int:
    """Rule: Determine the side length of the square output grid as the maximum of row and column spans."""
    return max(row_span, col_span)

def pad_rows_centered(grid: tp.List[tp.List[int]], target_n: int) -> tp.List[tp.List[int]]:
    """Transformation: Pad the grid with empty rows centered to reach target size N."""
    current_n = len(grid)
    if current_n >= target_n:
        return grid
    pad_total = target_n - current_n
    pad_top = pad_total // 2
    pad_bottom = pad_total - pad_top
    empty_row = [0] * len(grid[0])
    padded = [empty_row[:] for _ in range(pad_top)] + grid + [empty_row[:] for _ in range(pad_bottom)]
    return padded

def pad_columns_centered(grid: tp.List[tp.List[int]], target_n: int) -> tp.List[tp.List[int]]:
    """Transformation: Pad the grid with empty columns centered to reach target size N."""
    current_m = len(grid[0]) if grid else 0
    if current_m >= target_n:
        return grid
    pad_total = target_n - current_m
    pad_left = pad_total // 2
    pad_right = pad_total - pad_left
    padded = []
    for row in grid:
        new_row = [0] * pad_left + row + [0] * pad_right
        padded.append(new_row)
    return padded

def program(g: tp.List[tp.List[int]]) -> tp.List[tp.List[int]]:
    """Compose all rules to generate the output grid from input."""
    min_r, max_r = find_longest_consecutive_non_empty_rows(g)
    row_span = max_r - min_r + 1
    min_c, max_c = find_bounding_columns(g, min_r, max_r)
    col_span = max_c - min_c + 1
    N = compute_target_size(row_span, col_span)
    cropped = crop_to_bounding_box(g, min_r, max_r, min_c, max_c)
    padded_rows = pad_rows_centered(cropped, N)
    output = pad_columns_centered(padded_rows, N)
    return output
```