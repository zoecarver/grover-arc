```python
from typing import List, Tuple

def program(g: List[List[int]]) -> List[List[int]]:
    def find_bar(g: List[List[int]]) -> Tuple[int, int, int, int]:
        n_rows = len(g)
        if n_rows == 0:
            return 0, 0, 0, 0
        n_cols = len(g[0])
        max_h = 0
        best_r = best_c = best_w = 0
        for r in range(n_rows):
            row0 = g[r]
            bars: List[Tuple[int, int]] = []
            i = 0
            while i < n_cols:
                if row0[i] == 8:
                    j = i
                    while j < n_cols and row0[j] == 8:
                        j += 1
                    bars.append((i, j - i))
                    i = j
                else:
                    i += 1
            if not bars:
                continue
            c0, w0 = max(bars, key=lambda p: p[1])
            hh = 1
            while r + hh < n_rows:
                row = g[r + hh]
                if all(row[m] == 8 for m in range(c0, c0 + w0)):
                    hh += 1
                else:
                    break
            if hh > max_h:
                max_h = hh
                best_r = r
                best_c = c0
                best_w = w0
        return best_r, max_h, best_c, best_w

    r_start, h, c, w = find_bar(g)
    if h == 0 or w == 0:
        return []
    bar_set = set(range(r_start, r_start + h))
    n_rows = len(g)
    n_cols = len(g[0])
    output: List[List[int]] = []
    for k in range(h):
        i = r_start + k
        left = g[i][:c]
        right = g[i][c + w:]
        found = False
        for j in range(n_rows):
            if j == i or j in bar_set:
                continue
            j_left = g[j][:c]
            j_right = g[j][c + w:]
            if j_left == left and j_right == right:
                middle = g[j][c:c + w]
                output.append(middle)
                found = True
                break
        if not found:
            left_len = c
            right_len = n_cols - c - w
            if left_len >= right_len:
                for j in range(n_rows):
                    if j == i or j in bar_set:
                        continue
                    if g[j][:c] == left:
                        middle = g[j][c:c + w]
                        output.append(middle)
                        found = True
                        break
                if not found:
                    s = right_len + 2
                    vals = [g[i][s + jj] for jj in range(w)]
                    middle = vals[::-1]
                    output.append(middle)
            else:
                for j in range(n_rows):
                    if j == i or j in bar_set:
                        continue
                    if g[j][c + w:] == right:
                        middle = g[j][c:c + w]
                        output.append(middle)
                        found = True
                        break
                if not found:
                    s = left_len + 2
                    right_start = c + w
                    vals = [g[i][right_start + s + jj] for jj in range(w)]
                    middle = vals[::-1]
                    output.append(middle)
    return output
```