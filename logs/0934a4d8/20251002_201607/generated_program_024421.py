```python
from typing import List, Tuple

def find_bar(g: List[List[int]]) -> Tuple[int, int, int, int]:
    n_rows = len(g)
    if n_rows == 0:
        return 0, 0, 0, 0
    n_cols = len(g[0])
    max_h = 0
    best_r = best_c = best_w = 0
    for r in range(n_rows):
        bars = []
        ii = 0
        while ii < n_cols:
            if g[r][ii] == 8:
                jj = ii
                while jj < n_cols and g[r][jj] == 8:
                    jj += 1
                bars.append((ii, jj - ii))
                ii = jj
            else:
                ii += 1
        if not bars:
            continue
        c0, w0 = max(bars, key=lambda x: x[1])
        hh = 1
        while r + hh < n_rows:
            consistent = all(g[r + hh][cc] == 8 for cc in range(c0, c0 + w0))
            if not consistent:
                break
            hh += 1
        if hh > max_h:
            max_h = hh
            best_r = r
            best_c = c0
            best_w = w0
    return best_r, max_h, best_c, best_w

def program(g: List[List[int]]) -> List[List[int]]:
    r_start, h, c_start, w = find_bar(g)
    if h == 0:
        return []
    bar_rows = set(range(r_start, r_start + h))
    output = []
    left_len = c_start
    right_len = len(g[0]) - c_start - w
    left_slice = slice(0, left_len)
    right_slice = slice(c_start + w, None)
    middle_slice = slice(c_start, c_start + w)
    longer_is_left = left_len >= right_len
    shorter_len = right_len if longer_is_left else left_len
    n = len(g)
    for k in range(h):
        i = r_start + k
        left = g[i][left_slice]
        right = g[i][right_slice]
        middle = None
        # exact match
        for j in range(n):
            if j in bar_rows:
                continue
            if g[j][left_slice] == left and g[j][right_slice] == right:
                middle = g[j][middle_slice]
                break
        if middle is None:
            # partial on longer side
            if longer_is_left and left_len > 0:
                for j in range(n):
                    if j in bar_rows:
                        continue
                    if g[j][left_slice] == left:
                        middle = g[j][middle_slice]
                        break
            elif right_len > 0:
                for j in range(n):
                    if j in bar_rows:
                        continue
                    if g[j][right_slice] == right:
                        middle = g[j][middle_slice]
                        break
        if middle is None:
            # fallback reversal
            offset = shorter_len + 2
            if longer_is_left:
                sample_start = offset
                sample = g[i][sample_start:sample_start + w]
            else:
                sample_start = c_start + w + offset
                sample = g[i][sample_start:sample_start + w]
            middle = sample[::-1]
        output.append(middle)
    return output
```