```python
from typing import List

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return []
    h = len(g)
    w = len(g[0])
    col_nonzero = [0] * w
    col_color_sets = [set() for _ in range(w)]
    for r in range(h):
        for col in range(w):
            val = g[r][col]
            if val != 0:
                col_color_sets[col].add(val)
                col_nonzero[col] += 1
    best_score = -1
    s = -1
    spine_c = 0
    for col in range(w):
        if len(col_color_sets[col]) == 1:
            score = col_nonzero[col]
            if score > best_score:
                best_score = score
                s = col
                spine_c = list(col_color_sets[col])[0] if col_color_sets[col] else 0
    if s == -1:
        return [row[:] for row in g]
    new_g = [row[:] for row in g]
    for r in range(h):
        row = new_g[r]
        runs = []
        i = 0
        while i < s:
            if row[i] == 0:
                i += 1
                continue
            c = row[i]
            start = i
            while i < s and row[i] == c:
                i += 1
            l = i - start
            runs.append((c, l))
        right_w = w - s - 1
        pattern = [0] * right_w
        for c, l in runs:
            for p in range(0, right_w, l):
                pattern[p] = c
        orig_row = g[r]
        for p in range(right_w):
            col_pos = s + 1 + p
            if orig_row[col_pos] == 0:
                row[col_pos] = pattern[p]
    return new_g
```