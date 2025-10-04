```python
from typing import List, Tuple

def find_bar(g: List[List[int]]) -> Tuple[int, int, int, int]:
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

def recover_row(g: List[List[int]], i: int, c: int, w: int, bar_rows: set) -> List[int]:
    n = len(g)
    left_vis = g[i][0:c]
    right_vis = g[i][c + w:]
    left_len = len(left_vis)
    right_len = len(right_vis)
    # Try exact match
    for j in range(n):
        if j == i or j in bar_rows:
            continue
        j_left = g[j][0:c]
        j_right = g[j][c + w:]
        if j_left == left_vis and j_right == right_vis:
            middle = g[j][c:c + w]
            # apply swap if applicable for right
            if right_len >= 2:
                j_right_first2 = j_right[:2]
                i_right_first2 = right_vis[:2]
                if len(i_right_first2) == 2 and i_right_first2[0] == j_right_first2[1] and i_right_first2[1] == j_right_first2[0] and right_vis[2:] == j_right[2:]:
                    if w >= 3:
                        middle = list(middle)
                        middle[1], middle[2] = middle[2], middle[1]
            return middle
    # No exact, match on longer
    found = False
    middle = None
    if left_len >= right_len:
        # match on left
        for j in range(n):
            if j == i or j in bar_rows:
                continue
            j_left = g[j][0:c]
            if j_left == left_vis:
                middle = g[j][c:c + w]
                j_right = g[j][c + w:]
                if right_len >= 2:
                    j_right_first2 = j_right[:2]
                    i_right_first2 = right_vis[:2]
                    if len(i_right_first2) == 2 and i_right_first2[0] == j_right_first2[1] and i_right_first2[1] == j_right_first2[0] and right_vis[2:] == j_right[2:]:
                        if w >= 3:
                            middle = list(middle)
                            middle[1], middle[2] = middle[2], middle[1]
                found = True
                break
    else:
        # match on right
        for j in range(n):
            if j == i or j in bar_rows:
                continue
            j_right = g[j][c + w:]
            if j_right == right_vis:
                middle = g[j][c:c + w]
                j_left = g[j][0:c]
                if left_len >= 2:
                    j_left_first2 = j_left[:2]
                    i_left_first2 = left_vis[:2]
                    if len(i_left_first2) == 2 and i_left_first2[0] == j_left_first2[1] and i_left_first2[1] == j_left_first2[0] and left_vis[2:] == j_left[2:]:
                        if w >= 3:
                            middle = list(middle)
                            middle[1], middle[2] = middle[2], middle[1]
                found = True
                break
    if found:
        return middle
    # fallback to symmetric
    j = n - 1 - i
    if 0 <= j < n and j not in bar_rows and j != i:
        return g[j][c:c + w]
    # else 8's
    return [8] * w

def program(g: List[List[int]]) -> List[List[int]]:
    r_start, h, c, w = find_bar(g)
    bar_rows = set(range(r_start, r_start + h))
    output = []
    for k in range(h):
        i = r_start + k
        rec = recover_row(g, i, c, w, bar_rows)
        output.append(rec)
    return output
```