```python
from typing import List
from collections import Counter

def get_background(g: List[List[int]]) -> int:
    if not g or not g[0]:
        return 0
    flat = [cell for row in g for cell in row]
    if not flat:
        return 0
    return Counter(flat).most_common(1)[0][0]

def find_bounds(g: List[List[int]], start_r: int, end_r: int, bg: int, w: int) -> tuple:
    min_c = w
    max_c = -1
    for r in range(start_r, end_r + 1):
        for c in range(w):
            if g[r][c] != bg:
                min_c = min(min_c, c)
                max_c = max(max_c, c)
    return min_c, max_c

def build_subgrid(g: List[List[int]], start_r: int, left: int, right: int, num_rows: int) -> List[List[int]]:
    width = right - left + 1
    return [[g[start_r + dr][left + dc] for dc in range(width)] for dr in range(num_rows)]

def trim_columns_all(sub: List[List[int]], bg: int) -> List[List[int]]:
    if not sub or not sub[0]:
        return sub
    rows = len(sub)
    cols = len(sub[0])
    l = 0
    while l < cols:
        if all(sub[rr][l] == bg for rr in range(rows)):
            l += 1
        else:
            break
    r = cols - 1
    while r >= l:
        if all(sub[rr][r] == bg for rr in range(rows)):
            r -= 1
        else:
            break
    if l > r:
        return []
    return [row[l:r + 1] for row in sub]

def trim_framing(sub: List[List[int]], bg: int) -> List[List[int]]:
    if len(sub) != 5 or not sub[0]:
        return sub
    n = len(sub[0])
    # left frame
    non_bg_top = [j for j in range(n) if sub[0][j] != bg]
    if len(non_bg_top) == 1:
        f = non_bg_top[0]
        if sub[4][f] != bg:
            sub = [row[f + 1:] for row in sub]
    # right frame
    n = len(sub[0])
    if n > 0:
        non_bg_top = [j for j in range(n) if sub[0][j] != bg]
        if len(non_bg_top) == 1:
            f = non_bg_top[0]
            if f == n - 1 and sub[4][f] != bg:
                sub = [row[:f] for row in sub]
    return sub

def max_overlap(left_sub: List[List[int]], right_sub: List[List[int]]) -> int:
    if not left_sub or not right_sub or not left_sub[0] or not right_sub[0]:
        return 0
    w1 = len(left_sub[0])
    w2 = len(right_sub[0])
    max_k = min(w1, w2)
    for k in range(max_k, -1, -1):
        match = True
        for rr in range(5):
            if any(left_sub[rr][w1 - k + j] != right_sub[rr][j] for j in range(k)):
                match = False
                break
        if match:
            return k
    return 0

def has_color_one(g: List[List[int]], start_r: int, end_r: int, bg: int, w: int) -> bool:
    for r in range(start_r, end_r + 1):
        for c in range(w):
            if g[r][c] == 1 and 1 != bg:
                return True
    return False

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    h = len(g)
    if h == 0:
        return []
    w = len(g[0])
    bg = get_background(g)
    processed = set()
    slabs = []
    i = 0
    while i < h:
        if i in processed:
            i += 1
            continue
        has_start = any(g[i][c] != bg for c in range(w))
        if not has_start:
            i += 1
            continue
        added = False
        # Try 5-row
        if i + 4 < h:
            has_end = any(g[i + 4][c] != bg for c in range(w))
            if has_end:
                min_c, max_c = find_bounds(g, i, i + 4, bg, w)
                if min_c <= max_c:
                    sub = build_subgrid(g, i, min_c, max_c, 5)
                    sub = trim_columns_all(sub, bg)
                    sub = trim_framing(sub, bg)
                    if sub and sub[0]:
                        slabs.append((i, sub))
                        for rr in range(i, i + 5):
                            processed.add(rr)
                        i += 5
                        added = True
        # Fallback to 3-row if not added
        if not added and i + 2 < h:
            has_end3 = any(g[i + 2][c] != bg for c in range(w))
            if has_end3 and has_color_one(g, i, i + 2, bg, w):
                min_c, max_c = find_bounds(g, i, i + 2, bg, w)
                if min_c <= max_c:
                    sub3 = build_subgrid(g, i, min_c, max_c, 3)
                    sub3 = trim_columns_all(sub3, bg)
                    if sub3 and sub3[0]:
                        pad_row = [bg] * len(sub3[0])
                        sub = [pad_row] + sub3 + [pad_row]
                        sub = trim_framing(sub, bg)
                        if sub and sub[0]:
                            slabs.append((i, sub))
                            for rr in range(i, i + 3):
                                processed.add(rr)
                            i += 3
                            added = True
        if not added:
            i += 1
    if not slabs:
        return [[bg] for _ in range(5)]
    # Sort by decreasing start row
    slabs.sort(key=lambda x: -x[0])
    # Merge
    strip = [row[:] for row in slabs[0][1]]
    for _, s in slabs[1:]:
        k = max_overlap(strip, s)
        for rr in range(5):
            strip[rr].extend(s[rr][k:])
    return strip
```