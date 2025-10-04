```python
from typing import List

def count_nonzeros(row: List[int]) -> int:
    return sum(1 for x in row if x != 0)

def first_nonzero(row: List[int]) -> int:
    for j in range(len(row)):
        if row[j] != 0:
            return j
    return len(row)

def last_nonzero(row: List[int]) -> int:
    for j in range(len(row) - 1, -1, -1):
        if row[j] != 0:
            return j
    return -1

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    if n == 0:
        return [[0]]
    counts = [count_nonzeros(row) for row in g]
    # Find the longest contiguous block of non-empty rows
    max_len = 0
    best_start = 0
    best_end = -1
    curr_start = 0
    for i in range(n + 1):
        if i == n or counts[i] == 0:
            length = i - curr_start
            if length > max_len:
                max_len = length
                best_start = curr_start
                best_end = i - 1
            curr_start = i + 1
    if max_len == 0:
        return [[0]]
    start_r = best_start
    end_r = best_end
    # Compute min_c and max_c
    min_c = len(g[0]) if g else 0
    max_c = -1
    for i in range(start_r, end_r + 1):
        f = first_nonzero(g[i])
        l = last_nonzero(g[i])
        if l >= 0:
            min_c = min(min_c, f)
            max_c = max(max_c, l)
    if max_c < 0:
        return [[0]]
    # Crop the subgrid
    cropped = [g[i][min_c:max_c + 1] for i in range(start_r, end_r + 1)]
    h = len(cropped)
    w = len(cropped[0]) if h > 0 else 0
    s = max(h, w) if h > 0 and w > 0 else 1
    # Pad columns to s, centered
    if w < s:
        pad_left = (s - w) // 2
        pad_right = s - w - pad_left
        cropped = [[0] * pad_left + row + [0] * pad_right for row in cropped]
    # Pad rows to s, centered
    if h < s:
        pad_top = (s - h) // 2
        pad_bottom = s - h - pad_top
        empty_row = [0] * s
        cropped = [empty_row[:] for _ in range(pad_top)] + cropped + [empty_row[:] for _ in range(pad_bottom)]
    return cropped
```