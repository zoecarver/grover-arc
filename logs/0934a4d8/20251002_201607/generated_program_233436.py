```python
from typing import List

def find_bar(g: List[List[int]]) -> tuple:
    n = 30
    max_h = 0
    best_r, best_c, best_w = 0, 0, 0
    for r in range(n):
        for hh in range(1, n - r + 1):
            row0 = g[r]
            bars = []
            i = 0
            while i < n:
                if row0[i] == 8:
                    j = i
                    while j < n and row0[j] == 8:
                        j += 1
                    bars.append((i, j - i))
                    i = j
                else:
                    i += 1
            if not bars:
                continue
            c0, w0 = max(bars, key=lambda x: x[1])
            consistent = True
            for k in range(hh):
                row = g[r + k]
                bar_ok = all(row[m] == 8 for m in range(c0, c0 + w0))
                if not bar_ok:
                    consistent = False
                    break
            if consistent and hh > max_h:
                max_h = hh
                best_r = r
                best_c = c0
                best_w = w0
    return best_r, max_h, best_c, best_w

def recover_row(g: List[List[int]], i: int, c: int, w: int) -> List[int]:
    n = 30
    left_vis = g[i][0:c]
    right_vis = g[i][c + w:n]
    for j in range(n):
        if j == i:
            continue
        j_left = g[j][0:c]
        j_right = g[j][c + w:n]
        if j_left == left_vis and j_right == right_vis:
            return g[j][c:c + w]
    # Assume always found; fallback to empty if not
    return []

def program(g: List[List[int]]) -> List[List[int]]:
    r_start, h, c, w = find_bar(g)
    output = []
    for k in range(h):
        i = r_start + k
        rec = recover_row(g, i, c, w)
        output.append(rec)
    return output
```