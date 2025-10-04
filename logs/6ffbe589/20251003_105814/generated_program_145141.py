```python
from typing import List, Tuple

def row_nonzero_count(row: List[int]) -> int:
    """Counts the number of non-zero elements in a row for density analysis."""
    return sum(1 for x in row if x != 0)

def row_counts(g: List[List[int]]) -> List[int]:
    """Computes non-zero counts for each row in the grid."""
    return [row_nonzero_count(row) for row in g]

def find_longest_contiguous_nonzero_block(counts: List[int]) -> Tuple[int, int]:
    """Finds the start and end indices of the longest consecutive sequence of rows with >0 non-zeros."""
    n = len(counts)
    max_len = 0
    best_start = 0
    current_start = 0
    for i in range(n + 1):
        if i == n or counts[i] == 0:
            length = i - current_start
            if length > max_len:
                max_len = length
                best_start = current_start
            current_start = i + 1
    best_end = best_start + max_len - 1
    return best_start, best_end

def get_row_bounds(g: List[List[int]]) -> List[Tuple[int, int]]:
    """Computes the min and max non-zero column indices for each row (tight bounds per row)."""
    if not g:
        return []
    n_cols = len(g[0])
    bounds = []
    for row in g:
        first = n_cols
        last = -1
        for j in range(n_cols):
            if row[j] != 0:
                first = min(first, j)
                last = max(last, j)
        bounds.append((first, last))
    return bounds

def compute_max_tight_width(bounds: List[Tuple[int, int]]) -> int:
    """Computes the maximum tight width across all rows' bounds."""
    max_w = 0
    for f, l in bounds:
        if l >= 0:
            w = l - f + 1
            max_w = max(max_w, w)
    return max_w

def pad_row_to_size(row: List[int], size: int) -> List[int]:
    """Pads a single row centered with zeros to the target size."""
    curr_w = len(row)
    if curr_w >= size:
        return row
    left = (size - curr_w) // 2
    right = size - curr_w - left
    return [0] * left + row + [0] * right

def pad_rows_centered(rows: List[List[int]], size: int) -> List[List[int]]:
    """Pads the grid vertically centered with zero rows to the target size."""
    curr_h = len(rows)
    if curr_h >= size:
        return rows
    top = (size - curr_h) // 2
    bottom = size - curr_h - top
    zero_row = [0] * len(rows[0]) if rows else [0] * size
    padded = [zero_row[:] for _ in range(top)] + rows + [zero_row[:] for _ in range(bottom)]
    return padded

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program: Extracts the main pattern by per-row tight cropping and centered padding to square."""
    if not g or not g[0]:
        return [[0]]
    counts = row_counts(g)
    start, end = find_longest_contiguous_nonzero_block(counts)
    if start > end:
        return [[0]]
    h = end - start + 1
    bounds = get_row_bounds(g)
    max_w = compute_max_tight_width(bounds[start:end+1])
    s = max(h, max_w)
    output = []
    for i in range(start, end + 1):
        f, l = bounds[i]
        if l < 0:
            row_cropped = []
        else:
            row_cropped = g[i][f:l + 1]
        row_padded = pad_row_to_size(row_cropped, s)
        output.append(row_padded)
    # If h < s, pad vertically centered (though per-row already to s width)
    output = pad_rows_centered(output, s)
    return output
```