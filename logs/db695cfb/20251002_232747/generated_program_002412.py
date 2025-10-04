```python
from typing import List
from collections import defaultdict

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return []
    h, w = len(g), len(g[0])
    bg = g[0][0]
    new_grid = [row[:] for row in g]
    one_main = defaultdict(list)
    one_anti = defaultdict(list)
    six_main = defaultdict(list)
    six_anti = defaultdict(list)
    for r in range(h):
        for c in range(w):
            val = g[r][c]
            if val == 1:
                one_main[r - c].append(r)
                one_anti[r + c].append(r)
            elif val == 6:
                six_main[r - c].append(r)
                six_anti[r + c].append(r)
    trigger_anti = set()
    trigger_main = set()
    # Process main diagonals for 1s
    for d in one_main:
        rows1 = sorted(set(one_main[d]))
        if rows1:
            minr = rows1[0]
            maxr = rows1[-1]
            for r6 in six_main[d]:
                if minr < r6 < maxr:
                    c6 = r6 - d
                    if 0 <= c6 < w:
                        s = r6 + c6
                        trigger_anti.add(s)
            for r in range(minr, maxr + 1):
                c = r - d
                if 0 <= c < w and new_grid[r][c] == bg:
                    new_grid[r][c] = 1
    # Process anti diagonals for 1s
    for s in one_anti:
        rows1 = sorted(set(one_anti[s]))
        if rows1:
            minr = rows1[0]
            maxr = rows1[-1]
            for r6 in six_anti[s]:
                if minr < r6 < maxr:
                    c6 = s - r6
                    if 0 <= c6 < w:
                        d = r6 - c6
                        trigger_main.add(d)
            for r in range(minr, maxr + 1):
                c = s - r
                if 0 <= c < w and new_grid[r][c] == bg:
                    new_grid[r][c] = 1
    # Fill triggered main 6 diagonals
    for d in trigger_main:
        for r in range(h):
            c = r - d
            if 0 <= c < w and new_grid[r][c] == bg:
                new_grid[r][c] = 6
    # Fill triggered anti 6 diagonals
    for s in trigger_anti:
        for r in range(h):
            c = s - r
            if 0 <= c < w and new_grid[r][c] == bg:
                new_grid[r][c] = 6
    return new_grid
```