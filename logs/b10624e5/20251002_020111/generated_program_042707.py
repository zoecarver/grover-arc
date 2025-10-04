```python
from typing import List

def program(g: List[List[int]]) -> List[List[int]]:
    out = [row[:] for row in g]
    add_horizontal_mirror_top(out)
    add_vertical_mirror_bottom_left(out)
    add_180_mirror_bottom_right(out)
    return out

def add_horizontal_mirror_top(out: List[List[int]]):
    n = 27
    quad = 13
    conflict = any(out[r][n - 1 - c] != 4 and out[r][n - 1 - c] != out[r][c] for r in range(quad) for c in range(quad) if out[r][c] != 4)
    shift = 1 if conflict else 0
    for r in range(quad):
        tr = r - shift
        if tr < 0:
            continue
        for c in range(quad):
            if out[r][c] != 4:
                tc = n - 1 - c
                out[tr][tc] = out[r][c]

def add_vertical_mirror_bottom_left(out: List[List[int]]):
    n = 27
    quad = 13
    conflict = any(out[n - 1 - r][c] != 4 and out[n - 1 - r][c] != out[r][c] for r in range(quad) for c in range(quad) if out[r][c] != 4)
    shift = 1 if conflict else 0
    for r in range(quad):
        tr = n - 1 - r + shift
        if tr >= n:
            continue
        for c in range(quad):
            if out[r][c] != 4:
                tc = c
                out[tr][tc] = out[r][c]

def add_180_mirror_bottom_right(out: List[List[int]]):
    n = 27
    quad = 13
    conflict = any(out[n - 1 - r][n - 1 - c] != 4 and out[n - 1 - r][n - 1 - c] != out[r][c] for r in range(quad) for c in range(quad) if out[r][c] != 4)
    shift = 1 if conflict else 0
    for r in range(quad):
        tr = n - 1 - r + shift
        if tr >= n:
            continue
        for c in range(quad):
            if out[r][c] != 4:
                tc = n - 1 - c
                out[tr][tc] = out[r][c]
```