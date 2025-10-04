```python
from typing import List, Tuple

def is_empty(row: List[int]) -> bool:
    """Check if a row contains no non-zero elements."""
    for x in row:
        if x != 0:
            return False
    return True

def row_non_zeros(row: List[int]) -> int:
    """Count the number of non-zero elements in a row."""
    count = 0
    for x in row:
        if x != 0:
            count += 1
    return count

def find_row_bounds(row: List[int]) -> Tuple[int, int]:
    """Find the minimum and maximum column indices with non-zero elements in a row."""
    m = len(row)
    min_c = m
    max_c = -1
    for j in range(m):
        if row[j] != 0:
            if j < min_c:
                min_c = j
            if j > max_c:
                max_c = j
    return min_c, max_c

def get_all_row_bounds(g: List[List[int]]) -> List[Tuple[int, int]]:
    """Compute row bounds for all rows in the grid."""
    return [find_row_bounds(row) for row in g]

def find_main_block(g: List[List[int]]) -> Tuple[int, int]:
    """Find the start and end indices of the longest sequence of significant non-empty rows."""
    n = len(g)
    max_len = 0
    current_len = 0
    start = 0
    for i in range(n):
        if row_non_zeros(g[i]) > 2 or not is_empty(g[i]):
            current_len += 1
            if current_len > max_len:
                max_len = current_len
                start = i - current_len + 1
        else:
            current_len = 0
    end = start + max_len - 1
    return start, end

def compute_main_bounds(row_bounds: List[Tuple[int, int]], start: int, end: int) -> Tuple[int, int]:
    """Compute the overall min and max column bounds for the main block."""
    min_c = row_bounds[start][0]
    max_c = row_bounds[start][1]
    for i in range(start + 1, end + 1):
        min_c = min(min_c, row_bounds[i][0])
        max_c = max(max_c, row_bounds[i][1])
    return min_c, max_c

def crop_grid(g: List[List[int]], start: int, end: int, min_c: int, max_c: int) -> List[List[int]]:
    """Crop the grid to the main block and column bounds."""
    n_rows = end - start + 1
    cropped = []
    for i in range(start, end + 1):
        row = g[i][min_c:max_c + 1]
        cropped.append(row)
    return cropped

def pad_to_square(grid: List[List[int]]) -> List[List[int]]:
    """Pad the cropped grid to a square by adding zero rows and columns centered."""
    if not grid:
        return []
    h = len(grid)
    w = len(grid[0]) if h > 0 else 0
    size = max(h, w)
    pad_h_top = (size - h) // 2
    pad_h_bottom = size - h - pad_h_top
    pad_w_left = (size - w) // 2
    pad_w_right = size - w - pad_w_left
    new_grid = []
    for _ in range(pad_h_top):
        new_grid.append([0] * size)
    for row in grid:
        new_row = [0] * pad_w_left + row + [0] * pad_w_right
        new_grid.append(new_row)
    for _ in range(pad_h_bottom):
        new_grid.append([0] * size)
    return new_grid

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program: find main block, crop, and pad to square."""
    row_bounds = get_all_row_bounds(g)
    start, end = find_main_block(g)
    min_c, max_c = compute_main_bounds(row_bounds, start, end)
    cropped = crop_grid(g, start, end, min_c, max_c)
    result = pad_to_square(cropped)
    return result
```