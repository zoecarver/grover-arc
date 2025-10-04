```python
from typing import List, Tuple

def count_nonzeros(row: List[int]) -> int:
    """Count the number of non-zero elements in a row."""
    return sum(1 for x in row if x != 0)

def get_row_counts(g: List[List[int]]) -> List[int]:
    """Compute non-zero counts for each row in the grid."""
    return [count_nonzeros(row) for row in g]

def get_prefix_sums(counts: List[int]) -> List[int]:
    """Compute prefix sums of row counts for efficient range sum queries."""
    prefix = [0]
    for c in counts:
        prefix.append(prefix[-1] + c)
    return prefix

def find_max_sum_row_block(prefix: List[int]) -> Tuple[int, int]:
    """Find the contiguous row block with the maximum total non-zeros (allows internal empty rows)."""
    n = len(prefix) - 1
    max_sum = 0
    best_start = 0
    best_end = 0
    for i in range(n + 1):
        for j in range(i + 1, n + 2):
            current_sum = prefix[j - 1] - prefix[i]
            if current_sum > max_sum:
                max_sum = current_sum
                best_start = i
                best_end = j - 2  # Adjust for prefix indexing
    return best_start, best_end

def find_col_bounds(g: List[List[int]], start_r: int, end_r: int) -> Tuple[int, int]:
    """Find the minimal and maximal column indices with non-zeros in the row block."""
    n_cols = len(g[0]) if g and g[0] else 0
    min_c = n_cols
    max_c = -1
    has_nonzero = False
    for i in range(start_r, end_r + 1):
        row = g[i]
        for j in range(n_cols):
            if row[j] != 0:
                min_c = min(min_c, j)
                max_c = max(max_c, j)
                has_nonzero = True
    if not has_nonzero:
        return 0, 0
    return min_c, max_c

def crop_grid(g: List[List[int]], start_r: int, end_r: int, min_c: int, max_c: int) -> List[List[int]]:
    """Crop the grid to the specified row and column range (preserves relative positions)."""
    cropped = []
    for i in range(start_r, end_r + 1):
        row_slice = g[i][min_c:max_c + 1]
        cropped.append(row_slice)
    return cropped

def pad_to_square_size(cropped: List[List[int]]) -> List[List[int]]:
    """Pad the cropped grid to a square by adding zero rows and columns centered (global translation and padding rule)."""
    if not cropped:
        return [[0]]
    h = len(cropped)
    w = len(cropped[0]) if h > 0 else 0
    s = max(h, w)
    # Pad columns centered
    if w < s:
        pad_left = (s - w) // 2
        pad_right = s - w - pad_left
        for r in range(h):
            cropped[r] = [0] * pad_left + cropped[r] + [0] * pad_right
    # Pad rows centered
    if h < s:
        pad_top = (s - h) // 2
        pad_bottom = s - h - pad_top
        empty_row = [0] * s
        for _ in range(pad_top):
            cropped.insert(0, empty_row[:])
        for _ in range(pad_bottom):
            cropped.append(empty_row[:])
    return cropped

def remove_outliers_by_block(g: List[List[int]]) -> List[List[int]]:
    """Select the densest row block to exclude distant outliers (outlier removal rule)."""
    counts = get_row_counts(g)
    prefix = get_prefix_sums(counts)
    start_r, end_r = find_max_sum_row_block(prefix)
    if start_r > end_r:
        return [[0]]
    min_c, max_c = find_col_bounds(g, start_r, end_r)
    cropped = crop_grid(g, start_r, end_r, min_c, max_c)
    return cropped

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program: compose rules to crop main cluster, remove outliers, translate to top-left, pad to square."""
    cropped = remove_outliers_by_block(g)  # Outlier removal and main cluster selection
    squared = pad_to_square_size(cropped)  # Translation to top-left and centered padding to square
    return squared
```