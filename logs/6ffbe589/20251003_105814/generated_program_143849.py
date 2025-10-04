```python
from typing import List, Tuple
from collections import deque

def row_nonzero_count(row: List[int]) -> int:
    return sum(1 for x in row if x != 0)

def row_counts(g: List[List[int]]) -> List[int]:
    return [row_nonzero_count(row) for row in g]

def find_longest_block(counts: List[int]) -> Tuple[int, int]:
    n = len(counts)
    max_len = 0
    best_start = 0
    curr_start = 0
    for i in range(n + 1):
        if i == n or counts[i] == 0:
            length = i - curr_start
            if length > max_len:
                max_len = length
                best_start = curr_start
            curr_start = i + 1
    best_end = best_start + max_len - 1
    return best_start, best_end

def get_row_bounds(g: List[List[int]]) -> List[Tuple[int, int]]:
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

def compute_col_bounds(bounds: List[Tuple[int, int]], start_r: int, end_r: int, n_cols: int) -> Tuple[int, int]:
    min_c = n_cols
    max_c = -1
    for i in range(start_r, end_r + 1):
        f, l = bounds[i]
        if l >= 0:
            min_c = min(min_c, f)
            max_c = max(max_c, l)
    return min_c, max_c

def crop_subgrid(g: List[List[int]], start_r: int, end_r: int, min_c: int, max_c: int) -> List[List[int]]:
    cropped = []
    for i in range(start_r, end_r + 1):
        row = g[i][min_c : max_c + 1]
        cropped.append(row)
    return cropped

def pad_columns(cropped: List[List[int]], target_width: int) -> List[List[int]]:
    if not cropped:
        return []
    current_width = len(cropped[0])
    if current_width >= target_width:
        return cropped
    col_pad_left = (target_width - current_width) // 2
    col_pad_right = target_width - current_width - col_pad_left
    for r in range(len(cropped)):
        cropped[r] = [0] * col_pad_left + cropped[r] + [0] * col_pad_right
    return cropped

def pad_rows(cropped: List[List[int]], target_size: int) -> List[List[int]]:
    if not cropped:
        return []
    current_height = len(cropped)
    if current_height >= target_size:
        return cropped
    row_pad_top = (target_size - current_height) // 2
    row_pad_bottom = target_size - current_height - row_pad_top
    size = len(cropped[0])
    for _ in range(row_pad_top):
        cropped.insert(0, [0] * size)
    for _ in range(row_pad_bottom):
        cropped.append([0] * size)
    return cropped

def pad_to_square(cropped: List[List[int]]) -> List[List[int]]:
    if not cropped:
        return [[0]]
    h = len(cropped)
    w = len(cropped[0]) if h > 0 else 0
    s = max(h, w) if h > 0 and w > 0 else 1
    cropped = pad_columns(cropped, s)
    cropped = pad_rows(cropped, s)
    return cropped

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return [[0]]
    counts = row_counts(g)
    start_r, end_r = find_longest_block(counts)
    if start_r > end_r:
        return [[0]]
    n_cols = len(g[0])
    bounds = get_row_bounds(g)
    min_c, max_c = compute_col_bounds(bounds, start_r, end_r, n_cols)
    if min_c > max_c:
        return [[0]]
    cropped = crop_subgrid(g, start_r, end_r, min_c, max_c)
    return pad_to_square(cropped)
```