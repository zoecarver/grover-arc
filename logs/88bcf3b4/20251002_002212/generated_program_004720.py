```python
from typing import List
from collections import Counter

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    grid = [row[:] for row in g]
    flat = [cell for row in g for cell in row]
    count = Counter(flat)
    if not count:
        return grid
    bg = count.most_common(1)[0][0]
    positions = {}
    for i in range(n):
        for j in range(n):
            c = g[i][j]
            if c != bg:
                positions.setdefault(c, []).append((i, j))
    # Clear old positions
    for c in positions:
        for i, j in positions[c]:
            grid[i][j] = bg
    # Place each color vertically in its average column, stacked from min row up
    for c in positions:
        ps = positions[c]
        if not ps:
            continue
        cols = [j for _, j in ps]
        avg_col = sum(cols) // len(cols)
        rows = [i for i, _ in ps]
        min_row = min(rows)
        k = len(ps)
        for idx in range(k):
            r = min_row + idx
            if 0 <= r < n and 0 <= avg_col < n:
                grid[r][avg_col] = c
    return grid
```