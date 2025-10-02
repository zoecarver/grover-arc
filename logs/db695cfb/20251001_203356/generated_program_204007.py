```python
from typing import List, Set
from collections import defaultdict

def connect_blues_backslash(g: List[List[int]], out: List[List[int]], h: int, w: int, triggered_slash: Set[int]):
    for s in range(h + w - 1):
        rs = [r for r in range(max(0, s - w + 1), min(h, s + 1)) if 0 <= s - r < w and g[r][s - r] == 1]
        if len(rs) >= 2:
            rs = sorted(set(rs))
            minr = rs[0]
            maxr = rs[-1]
            for r in range(minr, maxr + 1):
                c = s - r
                if 0 <= c < w:
                    if g[r][c] not in {1, 6}:
                        out[r][c] = 1
                    elif g[r][c] == 6:
                        d = r - c
                        triggered_slash.add(d)

def connect_blues_slash(g: List[List[int]], out: List[List[int]], h: int, w: int, triggered_back: Set[int]):
    for d in range(-(w - 1), h):
        rs = [r for r in range(max(0, d), min(h, d + w)) if 0 <= r - d < w and g[r][r - d] == 1]
        if len(rs) >= 2:
            rs = sorted(set(rs))
            minr = rs[0]
            maxr = rs[-1]
            for r in range(minr, maxr + 1):
                c = r - d
                if 0 <= c < w:
                    if g[r][c] not in {1, 6}:
                        out[r][c] = 1
                    elif g[r][c] == 6:
                        s = r + c
                        triggered_back.add(s)

def fill_full_backslash(color: int, out: List[List[int]], h: int, w: int, sums_set: Set[int]):
    for s in sums_set:
        for r in range(max(0, s - w + 1), min(h, s + 1)):
            c = s - r
            if 0 <= c < w and out[r][c] not in {1, 6}:
                out[r][c] = color

def fill_full_slash(color: int, out: List[List[int]], h: int, w: int, diffs_set: Set[int]):
    for d in diffs_set:
        r_start = max(0, d)
        r_end = min(h, d + w)
        for r in range(r_start, r_end):
            c = r - d
            if 0 <= c < w and out[r][c] not in {1, 6}:
                out[r][c] = color

def extend_bottom(out: List[List[int]], h: int, w: int):
    if h < 2:
        return
    for c in range(w):
        bottom = out[h - 1][c]
        if bottom in {1, 6}:
            above = out[h - 2][c]
            if above not in {1, 6}:
                out[h - 2][c] = bottom

def program(g: List[List[int]]) -> List[List[int]]:
    h = len(g)
    if h == 0:
        return []
    w = len(g[0])
    out = [row[:] for row in g]
    triggered_back = set()
    triggered_slash = set()
    connect_blues_backslash(g, out, h, w, triggered_slash)
    connect_blues_slash(g, out, h, w, triggered_back)
    fill_full_backslash(6, out, h, w, triggered_back)
    fill_full_slash(6, out, h, w, triggered_slash)
    extend_bottom(out, h, w)
    return out
```