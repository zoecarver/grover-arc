```python
from typing import List, Tuple

def count_nonzeros(row: List[int]) -> int:
    return sum(x != 0 for x in row)

def get_counts(g: List[List[int]]) -> List[int]:
    return [count_nonzeros(row) for row in g]

def find_main_block(counts: List[int]) -> Tuple[int, int]:
    n = len(counts)
    max_len = 0
    best_start = 0
    curr_start = 0
    for i in range(n + 1):
        if i == n or counts[i] == 0:
            len_block = i - curr_start
            if len_block > max_len:
                max_len = len_block
                best_start = curr_start
            curr_start = i + 1
    best_end = best_start + max_len - 1
    return best_start, best_end

def get_row_bounds(g: List[List[int]]) -> List[Tuple[int, int]]:
    bounds = []
    for row in g:
        n = len(row)
        first = n
        last = -1
        for j in range(n):
            if row[j] != 0:
                first = min(first, j)
                last = max(last, j)
        bounds.append((first, last))
    return bounds

def compute_col_bounds(bounds: List[Tuple[int, int]], start_r: int, end_r: int, num_cols: int) -> Tuple[int, int]:
    min_c = num_cols
    max_c = -1
    for i in range(start_r, end_r + 1):
        f, l = bounds[i]
        if l != -1:
            min_c = min(min_c, f)
            max_c = max(max_c, l)
    return min_c, max_c

def crop_subgrid(g: List[List[int]], start_r: int, end_r: int, min_c: int, max_c: int) -> List[List[int]]:
    cropped = []
    for i in range(start_r, end_r + 1):
        row_slice = g[i][min_c : max_c + 1]
        cropped.append(row_slice)
    return cropped

def pad_dimension(lst: List[List[int]], target_size: int, is_rows: bool) -> List[List[int]]:
    if not lst:
        return [[0]]
    current_size = len(lst) if is_rows else len(lst[0])
    if current_size >= target_size:
        return lst
    pad_size = target_size - current_size
    left_or_top = pad_size // 2
    right_or_bottom = pad_size - left_or_top
    if is_rows:
        empty = [0] * len(lst[0])
        for _ in range(left_or_top):
            lst.insert(0, empty[:])
        for _ in range(right_or_bottom):
            lst.append(empty[:])
    else:
        for r in range(len(lst)):
            lst[r] = [0] * left_or_top + lst[r] + [0] * right_or_bottom
    return lst

def pad_to_square(cropped: List[List[int]]) -> List[List[int]]:
    if not cropped:
        return [[0]]
    h = len(cropped)
    w = len(cropped[0])
    size = max(h, w)
    cropped = pad_dimension(cropped, size, False)  # pad columns
    cropped = pad_dimension(cropped, size, True)   # pad rows
    return cropped

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return [[0]]
    num_cols = len(g[0])
    counts = get_counts(g)
    start_r, end_r = find_main_block(counts)
    if start_r > end_r:
        return [[0]]
    bounds = get_row_bounds(g)
    min_c, max_c = compute_col_bounds(bounds, start_r, end_r, num_cols)
    if max_c < 0:
        return [[0]]
    cropped = crop_subgrid(g, start_r, end_r, min_c, max_c)
    return pad_to_square(cropped)
```