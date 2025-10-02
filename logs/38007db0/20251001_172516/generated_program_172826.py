```python
from collections import Counter
from typing import List, Tuple

def get_border_color(g: List[List[int]]) -> int:
    return g[0][0] if g else 0

def get_wall_columns(g: List[List[int]], B: int) -> List[int]:
    H = len(g)
    if H == 0:
        return []
    W = len(g[0])
    walls = []
    for j in range(W):
        if all(g[i][j] == B for i in range(H)):
            walls.append(j)
    return walls

def get_patterns_for_row(g_row: List[int], walls: List[int]) -> List[Tuple[int, ...]]:
    patterns = []
    for k in range(len(walls) - 1):
        start = walls[k] + 1
        end = walls[k + 1]
        pat = tuple(g_row[start:end])
        patterns.append(pat)
    return patterns

def choose_pattern(patterns: List[Tuple[int, ...]]) -> List[int]:
    if not patterns:
        return []
    count = Counter(patterns)
    singles = [pat for pat, cnt in count.items() if cnt == 1]
    if singles:
        return list(singles[0])
    else:
        mc = count.most_common(1)[0][0]
        return list(mc)

def select_middle(chosen: List[int]) -> List[int]:
    return chosen[:5]

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    H = len(g)
    B = get_border_color(g)
    walls = get_wall_columns(g, B)
    out = []
    for i in range(H):
        g_row = g[i]
        if all(x == B for x in g_row):
            out_row = [B] * 7
        else:
            patterns = get_patterns_for_row(g_row, walls)
            chosen = choose_pattern(patterns)
            middle = select_middle(chosen)
            out_row = [B] + middle + [B]
        out.append(out_row)
    return out
```