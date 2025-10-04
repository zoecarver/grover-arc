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
        i = 0
        while i < m:
            if g[r][i] == 3:
                j = i
                while j < m and g[r][j] == 3:
                    j += 1
                length = j - i
                if length >= 3:
                    candidates.append((r, i, j - 1))
                i = j
            else:
                i += 1
    return candidates

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return []
    candidates = find_candidates(g)
    if len(candidates) < 2:
        return []
    candidates.sort(key=lambda x: x[0])
    top = candidates[0][0]
    bottom = candidates[-1][0]
    left = min(c[1] for c in candidates)
    right = max(c[2] for c in candidates)
    height = bottom - top + 1
    width = right - left + 1
    m = len(g[0])
    if height < 3 or width < 3 or width == m:
        return []
    # compute f: most common non-3 in inner area
    inner_colors = []
    for rr in range(top + 1, bottom):
        for cc in range(left + 1, right):
            color = g[rr][cc]
            if color != 3:
                inner_colors.append(color)
    if inner_colors:
        f = collections.Counter(inner_colors).most_common(1)[0][0]
    else:
        f = 3
    # build output
    output = []
    for i in range(height):
        r = top + i
        if i == 0 or i == height - 1:
            row = [3] * width
        else:
            row = [g[r][left + j] for j in range(width)]
            row[0] = 3
            row[-1] = 3
            # check if inner all 3's
            inner_start = 1
            inner_end = width - 1
            if inner_start < inner_end and all(x == 3 for x in row[inner_start:inner_end]):
                for j in range(inner_start, inner_end):
                    row[j] = f
        output.append(row)
    return output
```