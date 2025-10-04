```python
from typing import List
import collections

def find_3_candidates(g: List[List[int]]) -> List[tuple]:
    candidates = []
    n = len(g)
    if n == 0:
        return candidates
    m = len(g[0])
    for r in range(n):
        i = 0
        while i < m:
            if g[r][i] == 3:
                j = i
                while j < m and g[r][j] == 3:
                    j += 1
                length = j - i
                if length >= 6:
                    candidates.append((r, i, j - 1))
                i = j
            else:
                i += 1
    return candidates

def get_3_frame(g: List[List[int]], candidates: List[tuple]) -> tuple:
    if len(candidates) < 2:
        return None
    candidates = sorted(candidates, key=lambda x: x[0])
    top = candidates[0][0]
    bottom = candidates[-1][0]
    starts = [c[1] for c in candidates]
    ends = [c[2] for c in candidates]
    l = max(starts)
    r = min(ends)
    if l > r:
        return None
    h = bottom - top + 1
    w = r - l + 1
    m = len(g[0])
    if h < 3 or w < 3 or w == m:
        return None
    return top, bottom, l, r, h, w

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    if n == 0 or not g or not g[0]:
        return []
    m = len(g[0])
    candidates = find_3_candidates(g)
    frame = get_3_frame(g, candidates)
    if frame is None:
        return []
    top, bottom, l, r, h, w = frame
    # Compute fill: most common non-3 in inner subgrid
    inner_colors = []
    for rr in range(top, bottom + 1):
        for cc in range(l + 1, r):
            c = g[rr][cc]
            if c != 3:
                inner_colors.append(c)
    counter = collections.Counter(inner_colors)
    fill = counter.most_common(1)[0][0] if counter else 1
    # Build output
    output = []
    # Top border
    output.append([3] * w)
    # Inner rows
    for ii in range(1, h - 1):
        row_out = [3]
        for jj in range(l + 1, r):
            c = g[top + ii][jj]
            row_out.append(fill if c == 3 else c)
        row_out.append(3)
        output.append(row_out)
    # Bottom border
    output.append([3] * w)
    return output
```