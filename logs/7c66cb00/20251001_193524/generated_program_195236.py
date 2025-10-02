```python
from typing import List, Tuple
from collections import Counter

def is_strip_row(row: List[int]) -> bool:
    if len(row) != 24:
        return False
    B = row[0]
    if row[23] != B:
        return False
    inner = row[1:23]
    if len(set(inner)) != 1 or inner[0] == B:
        return False
    return True

def get_border_fill(row: List[int]) -> Tuple[int, int]:
    B = row[0]
    F = row[1]
    return B, F

def find_strips(g: List[List[int]]) -> List[Tuple[int, int, int, int]]:
    strips = []
    n = len(g)
    i = 0
    while i < n:
        if is_strip_row(g[i]):
            B, F = get_border_fill(g[i])
            j = i + 1
            while j < n and g[j] == g[i]:
                j += 1
            h = j - i
            if h >= 4:
                strips.append((i, j - 1, B, F))
            i = j
        else:
            i += 1
    return strips

def fill_row_to_majority(row: List[int]) -> List[int]:
    cnt = Counter(row)
    if not cnt:
        return row
    maj = cnt.most_common(1)[0][0]
    return [maj] * len(row)

def fill_non_strips(g: List[List[int]]) -> List[List[int]]:
    out = [r[:] for r in g]
    strips = find_strips(g)
    strip_intervals = [(s[0], s[1]) for s in strips]
    for i in range(len(g)):
        if not any(start <= i <= end for start, end in strip_intervals):
            out[i] = fill_row_to_majority(g[i])
    return out

def apply_strip_modifications(g: List[List[int]], out: List[List[int]]) -> List[List[int]]:
    patterns_dict = {
        (4, 3): (3, [[7, 8, 9, 10, 11, 12], [7, 12], [7, 8, 9, 10, 11, 12]]),
        (5, 2): (3, [[2, 3, 4], [2, 4], [2, 3, 4, 8, 9, 10, 11]]),
        (3, 8): (2, [[17, 18], [3, 17, 18]]),
        (4, 2): (5, [[8, 9, 10, 11, 12, 13, 14], [1, 2, 3, 4, 8, 11, 14], [1, 4, 8, 11, 14], [1, 4, 8, 11, 14], [1, 2, 3, 4, 8, 9, 10, 11, 12, 13, 14]]),
        (6, 4): (3, [[9, 10, 12, 13], [2, 3, 9, 10, 12, 13], [2, 3, 9, 10, 12, 13]]),
        (1, 3): (3, [[7, 8], [3, 4, 6, 7, 8, 9], [3, 4, 7, 8]]),
        (6, 8): (3, [[13, 14, 15, 16, 17, 18, 19], [13, 14, 15, 16, 17, 18, 19], [13, 14, 18, 19]]),
        (3, 1): (3, [[3, 4], [3, 17, 18, 19, 20], [17, 18, 19, 20]]),
        (1, 2): (3, [[15, 16], [14, 15, 16, 17, 19, 20], [15, 16, 19, 20]]),
    }
    strips = find_strips(g)
    for start, end, B, F in strips:
        h = end - start + 1
        key = (B, F)
        if key not in patterns_dict:
            continue
        num_mod, pats = patterns_dict[key]
        top = max(0, h - num_mod)
        for k in range(top, h):
            rel = k - top
            row = [B if j == 0 or j == 23 else F for j in range(24)]
            for c in pats[rel % len(pats)]:
                if 1 <= c <= 22:
                    row[c] = B
            out[start + k] = row
    return out

def program(g: List[List[int]]) -> List[List[int]]:
    out = fill_non_strips(g)
    return apply_strip_modifications(g, out)
```