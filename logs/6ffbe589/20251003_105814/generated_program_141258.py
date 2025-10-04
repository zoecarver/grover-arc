```python
from typing import List

def find_main_block(g: List[List[int]]) -> tuple:
    n = len(g)
    non_empty = [i for i in range(n) if any(cell != 0 for cell in g[i])]
    if not non_empty:
        return 0, 0, 0, 0, 1
    max_len = 0
    current_start = 0
    best_start = 0
    for k in range(1, len(non_empty) + 1):
        if k == len(non_empty) or non_empty[k] != non_empty[k - 1] + 1:
            length = non_empty[k - 1] - non_empty[current_start] + 1
            if length > max_len:
                max_len = length
                best_start = non_empty[current_start]
            current_start = k
    min_r = best_start
    max_r = min_r + max_len - 1
    h = max_len
    min_cs = []
    max_cs = []
    for i in range(min_r, max_r + 1):
        row_nonzero = [j for j in range(n) if g[i][j] != 0]
        if row_nonzero:
            min_cs.append(min(row_nonzero))
            max_cs.append(max(row_nonzero))
    if min_cs:
        min_c = min(min_cs)
        max_c = max(max_cs)
    else:
        min_c = 0
        max_c = 0
    w = max_c - min_c + 1 if max_c >= min_c else 1
    s = max(h, w)
    return min_r, max_r, min_c, max_c, s

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    min_r, max_r, min_c, max_c, s = find_main_block(g)
    h = max_r - min_r + 1
    w = max_c - min_c + 1
    pad_h = (s - h) // 2
    pad_w = (s - w) // 2
    new_g = []
    for i in range(s):
        if pad_h <= i < pad_h + h:
            di = i - pad_h
            row_slice = g[min_r + di][min_c : min_c + w]
            padded_row = [0] * pad_w + row_slice + [0] * (s - pad_w - w)
        else:
            padded_row = [0] * s
        new_g.append(padded_row)
    return new_g
```