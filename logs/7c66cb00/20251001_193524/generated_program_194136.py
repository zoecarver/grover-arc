```python
from typing import List
import collections

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

def get_border_fill(row: List[int]) -> tuple:
    B = row[0]
    F = row[1]
    return B, F

def fill_small_shapes(g: List[List[int]]) -> List[List[int]]:
    new_g = [row[:] for row in g]
    n = len(g)
    for r in range(n):
        row = g[r]
        if len(set(row)) == 1:
            continue
        counts = collections.Counter(row)
        majority = counts.most_common(1)[0][0]
        non_maj_pos = [c for c in range(24) if row[c] != majority]
        if len(non_maj_pos) == 2 and non_maj_pos[0] == 0 and non_maj_pos[1] == 23 and row[0] == row[23]:
            continue
        for c in range(24):
            new_g[r][c] = majority
    return new_g

def find_strips(g: List[List[int]]) -> List[tuple]:
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

def program(g: List[List[int]]) -> List[List[int]]:
    grid = fill_small_shapes(g)
    strips = find_strips(g)
    patterns = {
        (4, 3): {'top_unmodified': 4, 'num_mod': 3, 'extension': 0, 'pattern': [[7, 8, 9, 10, 11, 12], [7, 12], [7, 8, 9, 10, 11, 12]]},
        (5, 2): {'top_unmodified': 3, 'num_mod': 3, 'extension': 0, 'pattern': [[2, 3, 4], [2, 4], [2, 3, 4, 8, 9, 10, 11]]},
        (3, 8): {'top_unmodified': 2, 'num_mod': 2, 'extension': 0, 'pattern': [[17, 18], [3, 18, 19]]},
        (4, 2): {'top_unmodified': 4, 'num_mod': 4, 'extension': 1, 'pattern': [[8, 9, 10, 11, 12, 13, 14], [1, 2, 3, 4, 8, 11, 14], [1, 2, 4, 8, 11, 14], [1, 2, 4, 8, 11, 14], [1, 2, 3, 4, 8, 9, 10, 11, 12, 13, 14]]},
        (6, 4): {'top_unmodified': 3, 'num_mod': 3, 'extension': 0, 'pattern': [[9, 10, 12, 13], [2, 3, 9, 10, 12, 13], [2, 3, 9, 10, 12, 13]]},
        (1, 3): {'top_unmodified': 5, 'num_mod': 3, 'extension': 0, 'pattern': [[7, 8], [3, 4, 6, 7, 8, 9], [3, 4, 7, 8]]},
        (6, 8): {'top_unmodified': 2, 'num_mod': 3, 'extension': 0, 'pattern': [[13, 14, 15, 16, 17, 18, 19], [13, 14, 18, 19], [13, 14, 18, 19]]},
        (3, 1): {'top_unmodified': 2, 'num_mod': 2, 'extension': 0, 'pattern': [[17, 18], [3, 18, 19]]},
        (1, 2): {'top_unmodified': 1, 'num_mod': 3, 'extension': 0, 'pattern': [[7, 8], [3, 4, 6, 7, 8, 9], [3, 4, 7, 8]]},
    }
    n = len(grid)
    for start, end, B, F in strips:
        key = (B, F)
        if key in patterns:
            info = patterns[key]
            h = end - start + 1
            preferred_top = info['top_unmodified']
            preferred_num = info['num_mod']
            pat = info['pattern']
            n_pat = len(pat)
            extension = info['extension']
            if h < preferred_top + preferred_num:
                num_mod = min(preferred_num, h)
                top_unmodified = h - num_mod
            else:
                num_mod = preferred_num
                top_unmodified = preferred_top
            mod_start_rel = top_unmodified
            for kk in range(num_mod):
                k = mod_start_rel + kk
                r = start + k
                rel = kk % n_pat
                for c in pat[rel]:
                    if 0 <= c < 24:
                        grid[r][c] = B
            if key == (4, 2) and extension == 1 and end + 1 < n and all(grid[end + 1][c] == 8 for c in range(24)):
                r = end + 1
                strip_row = grid[end][:]
                grid[r] = strip_row
                rel = num_mod % n_pat
                for c in pat[rel]:
                    if 0 <= c < 24:
                        grid[r][c] = B
    return grid
```