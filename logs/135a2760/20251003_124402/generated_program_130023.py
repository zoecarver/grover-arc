```python
from typing import List

def program(g: List[List[int]]) -> List[List[int]]:
    new_g = [row[:] for row in g]
    if not g or not g[0]:
        return new_g
    h = len(g)
    w = len(g[0])
    s = g[0][0]
    period_dict = {1: 2, 3: 3, 4: 2, 8: 4, 9: 2}
    for r in range(h):
        row = new_g[r]
        if row[0] != s or row[w - 1] != s:
            continue
        if row[1] == row[w - 2] and row[1] != s:
            side = row[1]
            istart = 2
            iend = w - 3
        else:
            side = None
            istart = 1
            iend = w - 2
        if istart > iend:
            continue
        colors = set()
        for j in range(istart, iend + 1):
            val = row[j]
            if val != s and (side is None or val != side):
                colors.add(val)
        if len(colors) != 1:
            continue
        c = next(iter(colors))
        if c == 2:
            continue
        period = period_dict.get(c, 2)
        pattern = [c] * (period - 1) + [s]
        best_matches = -1
        best_phase = 0
        for phase in range(period):
            matches = 0
            for jj in range(istart, iend + 1):
                idx = (jj - istart + phase) % period
                if row[jj] == pattern[idx]:
                    matches += 1
            if matches > best_matches:
                best_matches = matches
                best_phase = phase
        for jj in range(istart, iend + 1):
            idx = (jj - istart + best_phase) % period
            new_g[r][jj] = pattern[idx]
    return new_g
```