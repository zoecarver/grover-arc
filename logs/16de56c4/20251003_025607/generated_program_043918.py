```python
from collections import defaultdict
from typing import List

def transform_line(original: List[int]) -> List[int]:
    n = len(original)
    pos_by_color: defaultdict[int, list[int]] = defaultdict(list)
    for p in range(n):
        c = original[p]
        if c != 0:
            pos_by_color[c].append(p)
    new = original[:]
    for c, poss in pos_by_color.items():
        if len(poss) != 2:
            continue
        p1, p2 = sorted(poss)
        d = p2 - p1
        positions = {p1, p2}
        color = c
        # Extend increasing direction
        max_p = p2
        while True:
            next_p = max_p + d
            if next_p >= n:
                break
            val = original[next_p]
            if val == 0:
                positions.add(next_p)
                max_p = next_p
            elif val == color:
                positions.add(next_p)
                max_p = next_p
            else:
                color = val
                positions.add(next_p)
                max_p = next_p
                break
        # Extend decreasing direction
        min_p = p1
        while True:
            next_p = min_p - d
            if next_p < 0:
                break
            val = original[next_p]
            if val == 0:
                positions.add(next_p)
                min_p = next_p
            elif val == color:
                positions.add(next_p)
                min_p = next_p
            else:
                color = val
                positions.add(next_p)
                min_p = next_p
                break
        # Set final color on positions
        for p in positions:
            new[p] = color
    return new

def apply_horizontal(g: List[List[int]]) -> List[List[int]]:
    h = len(g)
    if h == 0:
        return []
    w = len(g[0])
    new_g = [row[:] for row in g]
    for i in range(h):
        new_g[i] = transform_line(g[i])
    return new_g

def apply_vertical(g: List[List[int]]) -> List[List[int]]:
    h = len(g)
    if h == 0:
        return []
    w = len(g[0])
    new_g = [row[:] for row in g]
    for j in range(w):
        col = [g[i][j] for i in range(h)]
        new_col = transform_line(col)
        for i in range(h):
            new_g[i][j] = new_col[i]
    return new_g

def program(g: List[List[int]]) -> List[List[int]]:
    h = len(g)
    if h == 0:
        return []
    w = len(g[0])
    if h > w:
        return apply_horizontal(g)
    else:
        return apply_vertical(g)
```