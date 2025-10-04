```python
from typing import List, Tuple, Set

def find_tallest_eight_bar(g: List[List[int]]) -> Tuple[int, int, int, int]:
    """
    Finds the tallest consistent rectangular bar of 8's across consecutive rows,
    prioritizing maximum height, then maximum width within that height.
    Returns (start_row, height, start_col, width); (0, 0, 0, 0) if none found.
    """
    n_rows = len(g)
    if n_rows == 0:
        return 0, 0, 0, 0
    n_cols = len(g[0])
    max_h = 0
    best_r, best_c, best_w = 0, 0, 0
    for r in range(n_rows):
        # Find horizontal bars in starting row r
        bars: List[Tuple[int, int]] = []
        i = 0
        while i < n_cols:
            if g[r][i] == 8:
                j = i
                while j < n_cols and g[r][j] == 8:
                    j += 1
                bars.append((i, j - i))
                i = j
            else:
                i += 1
        if not bars:
            continue
        # Select widest bar in row r
        c0, w0 = max(bars, key=lambda p: p[1])
        # Extend vertically to find consistent height
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

def recover_middle_exact(g: List[List[int]], i: int, c: int, w: int, bar_rows: Set[int]) -> List[int]:
    """
    Recovers middle by finding a non-bar row j with exact matching left and right segments.
    Returns the middle from j if found, else empty list.
    """
    left_vis = g[i][:c]
    right_vis = g[i][c + w:]
    n = len(g)
    for j in range(n):
        if j in bar_rows:
            continue
        if g[j][:c] == left_vis and g[j][c + w:] == right_vis:
            return g[j][c:c + w]
    return []

def recover_middle_partial(g: List[List[int]], i: int, c: int, w: int, bar_rows: Set[int]) -> List[int]:
    """
    Recovers middle by partial matching on the longer visible side (left or right).
    Returns the middle from matching j if found, else empty list.
    """
    left_len = c
    right_len = len(g[0]) - c - w
    left_vis = g[i][:c]
    right_vis = g[i][c + w:]
    n = len(g)
    if left_len >= right_len and left_len > 0:
        # Match on left
        for j in range(n):
            if j in bar_rows:
                continue
            if g[j][:c] == left_vis:
                return g[j][c:c + w]
    elif right_len > 0:
        # Match on right
        for j in range(n):
            if j in bar_rows:
                continue
            if g[j][c + w:] == right_vis:
                return g[j][c:c + w]
    return []

def recover_middle_fallback_reverse(g: List[int], i: int, c: int, w: int, left_len: int, right_len: int) -> List[int]:
    """
    Fallback recovery: sample w elements from the longer side, offset by shorter_len + 2, and reverse.
    Handles cases with no exact or partial matches.
    """
    shorter_len = min(left_len, right_len)
    offset = shorter_len + 2
    if left_len >= right_len:
        sample_start = offset
        sample_end = sample_start + w
        if sample_end > len(g[i]):
            return [8] * w  # Fallback to 8's if out of bounds
        sample = g[i][sample_start:sample_end]
    else:
        sample_start = c + w + offset
        sample_end = sample_start + w
        if sample_end > len(g[i]):
            return [8] * w  # Fallback to 8's if out of bounds
        sample = g[i][sample_start:sample_end]
    return sample[::-1]

def recover_middle_for_row(g: List[List[int]], i: int, c: int, w: int, bar_rows: Set[int]) -> List[int]:
    """
    Composes recovery rules: try exact match, then partial on longer side, then reverse fallback.
    """
    exact = recover_middle_exact(g, i, c, w, bar_rows)
    if exact:
        return exact
    left_len = c
    right_len = len(g[0]) - c - w
    partial = recover_middle_partial(g, i, c, w, bar_rows)
    if partial:
        return partial
    return recover_middle_fallback_reverse(g, i, c, w, left_len, right_len)

def program(g: List[List[int]]) -> List[List[int]]:
    """
    Main program: finds the tallest 8-bar, recovers middles for each bar row using composed rules.
    """
    r_start, h, c, w = find_tallest_eight_bar(g)
    if h == 0:
        return []
    bar_rows: Set[int] = set(range(r_start, r_start + h))
    output: List[List[int]] = []
    for k in range(h):
        i = r_start + k
        middle = recover_middle_for_row(g, i, c, w, bar_rows)
        output.append(middle)
    return output
```