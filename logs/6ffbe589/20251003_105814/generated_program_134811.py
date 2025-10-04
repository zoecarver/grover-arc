```python
from typing import List, Tuple

def find_longest_consecutive_nonempty_rows(g: List[List[int]]) -> Tuple[int, int]:
    """Find the start and end row indices of the longest consecutive sequence of rows with at least one non-zero element."""
    n = len(g)
    max_length = 0
    best_start = 0
    best_end = -1
    current_start = 0
    for i in range(n):
        if sum(g[i]) == 0:
            length = i - current_start
            if length > max_length:
                max_length = length
                best_start = current_start
                best_end = i - 1
            current_start = i + 1
    length = n - current_start
    if length > max_length:
        max_length = length
        best_start = current_start
        best_end = n - 1
    return best_start, best_end

def find_bounding_columns(g: List[List[int]], min_r: int, max_r: int) -> Tuple[int, int]:
    """Find the minimal and maximal column indices that have at least one non-zero in the given row range."""
    n = len(g[0])
    has_nonzero = [any(g[r][c] != 0 for r in range(min_r, max_r + 1)) for c in range(n)]
    min_c = min((c for c in range(n) if has_nonzero[c]), default=0)
    max_c = max((c for c in range(n) if has_nonzero[c]), default=n - 1)
    return min_c, max_c

def create_padded_subgrid(g: List[List[int]], min_r: int, max_r: int, min_c: int, max_c: int) -> List[List[int]]:
    """Extract the subgrid from the given bounds and pad to a square of side max(h, w), centered."""
    h = max_r - min_r + 1
    w = max_c - min_c + 1
    size = max(h, w)
    top_pad = (size - h) // 2
    bottom_pad = size - h - top_pad
    left_pad = (size - w) // 2
    right_pad = size - w - left_pad
    # Extract subgrid
    sub_rows = [[g[min_r + i][min_c + j] for j in range(w)] for i in range(h)]
    # Pad subgrid horizontally
    padded_sub = [[ [0] * left_pad + sub_rows[i] + [0] * right_pad ] for i in range(h)]
    # Pad vertically with zero rows
    output = [[0] * size for _ in range(top_pad)] + padded_sub + [[0] * size for _ in range(bottom_pad)]
    return output

def program(g: List[List[int]]) -> List[List[int]]:
    min_r, max_r = find_longest_consecutive_nonempty_rows(g)
    min_c, max_c = find_bounding_columns(g, min_r, max_r)
    return create_padded_subgrid(g, min_r, max_r, min_c, max_c)
```