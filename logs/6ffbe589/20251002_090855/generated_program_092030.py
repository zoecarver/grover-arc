```python
from typing import List

def max_subarray_indices(arr: List[int]) -> tuple:
    n = len(arr)
    if n == 0:
        return 0, -1
    max_current = max_global = arr[0]
    current_start = 0
    global_start = 0
    global_end = 0
    for i in range(1, n):
        if arr[i] > max_current + arr[i]:
            max_current = arr[i]
            current_start = i
        else:
            max_current += arr[i]
        if max_current > max_global:
            max_global = max_current
            global_start = current_start
            global_end = i
    return global_start, global_end

def program(g: List[List[int]]) -> List[List[int]]:
    n = 20
    row_nonzero = [sum(x > 0 for x in row) for row in g]
    start, end = max_subarray_indices(row_nonzero)
    if start > end:
        return [[0] * n for _ in range(n)]  # fallback
    # initial min_c, max_c
    min_c = n
    max_c = -1
    for i in range(start, end + 1):
        for j in range(n):
            if g[i][j] > 0:
                min_c = min(min_c, j)
                max_c = max(max_c, j)
    width = max_c - min_c + 1 if max_c >= min_c else 0
    size = width
    # trim
    current_start = start
    current_end = end
    while current_end - current_start + 1 > size and current_start <= current_end:
        left = row_nonzero[current_start]
        right = row_nonzero[current_end]
        if left < right:
            current_start += 1
        else:
            current_end -= 1
    # additional trim small ends
    while current_start <= current_end and row_nonzero[current_start] < 2:
        current_start += 1
    while current_start <= current_end and row_nonzero[current_end] < 2:
        current_end -= 1
    height = current_end - current_start + 1 if current_start <= current_end else 0
    if height == 0:
        return [[0] * size for _ in range(size)]
    # update min_c, max_c
    min_c = n
    max_c = -1
    for i in range(current_start, current_end + 1):
        for j in range(n):
            if g[i][j] > 0:
                min_c = min(min_c, j)
                max_c = max(max_c, j)
    width = max_c - min_c + 1 if max_c >= min_c else 0
    size = max(height, width)
    # crop
    cropped = [g[i][min_c : max_c + 1] for i in range(current_start, current_end + 1)]
    # pad to square
    pad_h = size - height
    pad_w = size - width
    pad_top = pad_h // 2
    pad_bottom = pad_h - pad_top
    pad_left = pad_w // 2
    pad_right = pad_w - pad_left
    result = []
    for _ in range(pad_top):
        result.append([0] * size)
    for row in cropped:
        new_row = [0] * pad_left + row + [0] * pad_right
        result.append(new_row)
    for _ in range(pad_bottom):
        result.append([0] * size)
    return result
```