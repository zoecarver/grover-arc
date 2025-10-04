```python
from typing import List
import collections

def find_candidates(g: List[List[int]]) -> List[tuple]:
    candidates = []
    n = len(g)
    if n == 0:
        return candidates
    m = len(g[0])
    for r in range(n):
        c = 0
        while c < m:
            if g[r][c] == 3:
                start = c
                while c < m and g[r][c] == 3:
                    c += 1
                length = c - start
                if length > 4:
                    candidates.append((r, start, c - 1))
            else:
                c += 1
    return candidates

def program(g: List[List[int]]) -> List[List[int]]:
    candidates = find_candidates(g)
    if len(candidates) < 2:
        return []
    # Since all for b=3, single group
    candidates.sort(key=lambda x: x[0])
    top = candidates[0][0]
    bottom = candidates[-1][0]
    l = max(c[1] for c in candidates)
    r = min(c[2] for c in candidates)
    if l > r:
        return []
    w = r - l + 1
    if w < 5:
        return []
    h = bottom - top + 2
    # Extract h rows starting from top
    output = []
    n = len(g)
    inner_colors = []
    for i in range(h):
        rr = top + i
        if rr < n:
            sub = g[rr][l:r + 1]
            # Collect for f
            for jj in range(1, len(sub) - 1):
                col = sub[jj]
                if col != 3:
                    inner_colors.append(col)
        else:
            sub = [0] * w
        sub[0] = 3
        sub[-1] = 3
        output.append(sub)
    # Compute f
    if inner_colors:
        counter = collections.Counter(inner_colors)
        f = counter.most_common(1)[0][0]
    else:
        f = 0
    # Set top and bottom all 3's
    output[0] = [3] * w
    output[-1] = [3] * w
    # Fill uniform 3 inner rows
    for i in range(1, h - 1):
        inner = output[i][1:w - 1]
        if all(x == 3 for x in inner):
            for j in range(1, w - 1):
                output[i][j] = f
    return output
```