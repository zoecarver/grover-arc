```python
from typing import List
import collections

def find_background(g: List[List[int]]) -> int:
    if not g or not g[0]:
        return 0
    flat = [cell for row in g for cell in row]
    count = collections.Counter(flat)
    return count.most_common(1)[0][0]

def decide_group(c: int, has7: bool, has9: bool) -> str:
    if c == 3:
        return 'top'
    if c == 4:
        return 'bottom'
    if c == 1:
        return 'bottom' if has9 else 'top'
    if c == 2:
        return 'top' if has7 else 'bottom'
    if c in (7, 9):
        return 'top'
    return 'top'

def program(g: List[List[int]]) -> List[List[int]]:
    h = len(g)
    if h == 0:
        return []
    w = len(g[0])
    bg = find_background(g)
    color_positions = collections.defaultdict(list)
    for r in range(h):
        for c in range(w):
            val = g[r][c]
            if val != bg:
                color_positions[val].append((r, c))
    all_colors = list(color_positions.keys())
    has7 = 7 in all_colors
    has9 = 9 in all_colors
    out = [[bg for _ in range(w)] for _ in range(h)]
    for c in all_colors:
        pos_list = color_positions[c]
        if not pos_list:
            continue
        group = decide_group(c, has7, has9)
        rs = [p[0] for p in pos_list]
        min_r = min(rs)
        max_r = max(rs)
        if group == 'top':
            delta = -min_r
            for r, cc in pos_list:
                nr = r + delta
                out[nr][cc] = c
        else:  # bottom
            delta = (h - 1) - max_r
            for r, cc in pos_list:
                nr = r + delta
                out[nr][cc] = c
    return out
```