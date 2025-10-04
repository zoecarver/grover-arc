```python
from typing import List, Tuple

def compute_row_nonzero(g: List[List[int]]) -> List[int]:
    return [sum(1 for x in row if x > 0) for row in g]

def max_subarray_indices_with_max_gap(arr: List[int], max_gap: int) -> Tuple[int, int]:
    n = len(arr)
    best_sum = -1
    best_start = best_end = 0
    for s in range(n):
        current_sum = 0
        max_c_gap = 0
        current_gap = 0
        for e in range(s, n):
            if arr[e] > 0:
                current_sum += arr[e]
                current_gap = 0
            else:
                current_gap += 1
                max_c_gap = max(max_c_gap, current_gap)
            if max_c_gap <= max_gap:
                length = e - s + 1
                update = False
                if current_sum > best_sum:
                    update = True
                elif current_sum == best_sum:
                    best_length = best_end - best_start + 1 if best_end >= best_start else 0
                    if length > best_length:
                        update = True
                if update:
                    best_sum = current_sum
                    best_start = s
                    best_end = e
            else:
                break
    return best_start, best_end

def program(g: List[List[int]]) -> List[List[int]]:
    row_nonzero = compute_row_nonzero(g)
    start_r, end_r = max_subarray_indices_with_max_gap(row_nonzero, 1)
    n = len(g)
    if start_r > end_r:
        return [[0] * n for _ in range(n)]
    h = end_r - start_r + 1
    col_nonzero = [0] * n
    for c in range(n):
        for r in range(start_r, end_r + 1):
            if g[r][c] > 0:
                col_nonzero[c] += 1
    start_c, end_c = max_subarray_indices_with_max_gap(col_nonzero, 0)
    if start_c > end_c:
        start_c = n
        end_c = -1
        for c in range(n):
            if col_nonzero[c] > 0:
                start_c = min(start_c, c)
                end_c = max(end_c, c)
    w = end_c - start_c + 1 if start_c <= end_c else 0
    side = max(h, w)
    sub = [row[start_c:end_c + 1] for row in g[start_r:end_r + 1]]
    pad_top = (side - h) // 2
    pad_bottom = side - h - pad_top
    pad_left = (side - w) // 2
    pad_right = side - w - pad_left
    padded = [[0] * side for _ in range(side)]
    for i in range(h):
        for j in range(w):
            padded[pad_top + i][pad_left + j] = sub[i][j]
    return padded
```