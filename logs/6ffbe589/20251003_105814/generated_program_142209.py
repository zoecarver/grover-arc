```python
from typing import List

def row_nonzero_count(row: List[int]) -> int:
    count = 0
    for x in row:
        if x != 0:
            count += 1
    return count

def row_counts(g: List[List[int]]) -> List[int]:
    return [row_nonzero_count(row) for row in g]

def find_max_count_row(counts: List[int]) -> int:
    if not counts:
        return 0
    max_i = 0
    max_c = counts[0]
    for i in range(1, len(counts)):
        if counts[i] > max_c:
            max_c = counts[i]
            max_i = i
    return max_i

def find_start_row(counts: List[int], start: int) -> int:
    s = start
    while s > 0 and counts[s - 1] > 0:
        s -= 1
    return s

def find_end_row(counts: List[int], start: int) -> int:
    e = start
    n = len(counts)
    while e < n - 1 and counts[e + 1] > 0:
        e += 1
    return e

def get_row_bounds(g: List[List[int]]) -> List[tuple[int, int]]:
    bounds = []
    n_cols = len(g[0]) if g else 0
    for row in g:
        first = n_cols
        last = -1
        for j in range(n_cols):
            if row[j] != 0:
                first = min(first, j)
                last = max(last, j)
        bounds.append((first, last))
    return bounds

def compute_col_bounds(bounds: List[tuple[int, int]], start_r: int, end_r: int, n_cols: int) -> tuple[int, int]:
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

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return [[0]]
    n_rows = len(g)
    n_cols = len(g[0])
    counts = row_counts(g)
    max_i = find_max_count_row(counts)
    start_r = find_start_row(counts, max_i)
    end_r = find_end_row(counts, max_i)
    bounds = get_row_bounds(g)
    min_c, max_c = compute_col_bounds(bounds, start_r, end_r, n_cols)
    if max_c < 0:
        return [[0]]
    cropped = crop_subgrid(g, start_r, end_r, min_c, max_c)
    h = len(cropped)
    w = len(cropped[0]) if h > 0 else 0
    s = max(h, w)
    cropped = pad_columns(cropped, s)
    cropped = pad_rows(cropped, s)
    return cropped
```