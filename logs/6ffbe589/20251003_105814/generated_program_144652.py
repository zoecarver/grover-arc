```python
from typing import List, Tuple

def row_nonzero_counts(g: List[List[int]]) -> List[int]:
    return [sum(1 for x in row if x != 0) for row in g]

def find_max_sum_positive_segment_indices(arr: List[int]) -> Tuple[int, int]:
    n = len(arr)
    best_start = -1
    best_end = -1
    best_sum = -1
    i = 0
    while i < n:
        if arr[i] == 0:
            i += 1
            continue
        current_start = i
        current_sum = 0
        while i < n and arr[i] > 0:
            current_sum += arr[i]
            i += 1
        current_end = i - 1
        if current_sum > best_sum:
            best_sum = current_sum
            best_start = current_start
            best_end = current_end
    return best_start, best_end if best_start != -1 else (0, -1)

def col_nonzero_counts(selected_g: List[List[int]]) -> List[int]:
    if not selected_g:
        return []
    n_cols = len(selected_g[0])
    counts = [0] * n_cols
    for row in selected_g:
        for j in range(n_cols):
            if row[j] != 0:
                counts[j] += 1
    return counts

def crop_subgrid(g: List[List[int]], start_r: int, end_r: int, start_c: int, end_c: int) -> List[List[int]]:
    return [row[start_c:end_c + 1] for row in g[start_r:end_r + 1]]

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
    if not cropped or not any(any(x != 0 for x in row) for row in cropped):
        return [[0]]
    h = len(cropped)
    w = len(cropped[0]) if h > 0 else 0
    s = max(h, w)
    cropped = pad_columns(cropped, s)
    cropped = pad_rows(cropped, s)
    return cropped

def program(g: List[List[int]]) -> List[List[int]]:
    row_counts = row_nonzero_counts(g)
    row_start, row_end = find_max_sum_positive_segment_indices(row_counts)
    if row_start > row_end:
        return [[0]]
    selected_g = g[row_start:row_end + 1]
    col_counts = col_nonzero_counts(selected_g)
    col_start, col_end = find_max_sum_positive_segment_indices(col_counts)
    if col_start > col_end:
        h = row_end - row_start + 1
        zero_rows = [[0] * h for _ in range(h)]  # but unlikely
        return pad_to_square(zero_rows)
    cropped = crop_subgrid(g, row_start, row_end, col_start, col_end)
    return pad_to_square(cropped)
```