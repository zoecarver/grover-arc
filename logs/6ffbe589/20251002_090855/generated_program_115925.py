```python
from typing import List

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    def count_non0(row: List[int]) -> int:
        return sum(1 for x in row if x != 0)
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + count_non0(g[i])
    max_density = -1.0
    best_s = 0
    best_e = 1
    for s in range(n):
        for e in range(s + 1, n + 1):
            total = prefix[e] - prefix[s]
            area = (e - s) * n
            if area > 0:
                density = total / area
                if density > max_density:
                    max_density = density
                    best_s = s
                    best_e = e
    h = best_e - best_s
    min_c = n
    max_c = -1
    for i in range(best_s, best_e):
        for j in range(n):
            if g[i][j] != 0:
                if j < min_c:
                    min_c = j
                if j > max_c:
                    max_c = j
    w = max_c - min_c + 1 if max_c >= min_c else 0
    size = max(h, w)
    pad_top = (size - h) // 2
    pad_bottom = size - h - pad_top
    pad_left = (size - w) // 2
    pad_right = size - w - pad_left
    new_g: List[List[int]] = []
    for _ in range(pad_top):
        new_g.append([0] * size)
    for ii in range(h):
        i = best_s + ii
        row_slice = g[i][min_c:max_c + 1]
        padded_row = [0] * pad_left + row_slice + [0] * pad_right
        new_g.append(padded_row)
    for _ in range(pad_bottom):
        new_g.append([0] * size)
    return new_g
```