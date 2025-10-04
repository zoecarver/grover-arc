```python
from typing import List

def has_vertical_three(g: List[List[int]], i: int, c: int) -> bool:
    h = len(g)
    w = len(g[0]) if h > 0 else 0
    if i + 2 >= h or c >= w:
        return False
    return g[i][c] == 4 and g[i + 1][c] == 4 and g[i + 2][c] == 4

def has_horizontal_wings(g: List[List[int]], row: int, c: int) -> bool:
    h = len(g)
    w = len(g[0]) if h > 0 else 0
    if row >= h or c < 1 or c + 1 >= w:
        return False
    return g[row][c - 1] == 4 and g[row][c] == 4 and g[row][c + 1] == 4

def apply_pattern_fill(out: List[List[int]], i: int, c: int) -> None:
    out[i][c] = 8
    out[i + 1][c - 1] = 8
    out[i + 1][c] = 8
    out[i + 1][c + 1] = 8
    out[i + 2][c] = 8

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return []
    h = len(g)
    w = len(g[0])
    out = [row[:] for row in g]
    for i in range(h - 2):
        for c in range(1, w - 1):
            if has_vertical_three(out, i, c) and has_horizontal_wings(out, i + 1, c):
                apply_pattern_fill(out, i, c)
    return out
```