```python
from typing import List
import copy

def is_block_row(row: List[int]) -> bool:
    if len(row) != 24 or row[0] != row[23]:
        return False
    return row[0] != row[1]

def fill_background(g: List[List[int]]) -> List[List[int]]:
    g = copy.deepcopy(g)
    if len(g) == 0 or len(g[0]) == 0:
        return g
    bg = g[0][0]
    for row in g:
        non_bg_count = 0
        for c in row:
            if c != bg:
                non_bg_count += 1
        if non_bg_count < 10:
            for j in range(len(row)):
                row[j] = bg
    return g

def apply_h_pattern(g: List[List[int]], start: int, end: int, border_c: int, interior_c: int) -> None:
    height = end - start + 1
    k = min(3, height)
    for j in range(k):
        r = end - j
        row = g[r]
        for c in range(1, 23):
            row[c] = interior_c
        pattern_r = 2 - j
        if pattern_r == 0 or pattern_r == 2:
            for c in range(7, 13):
                row[c] = border_c
        elif pattern_r == 1:
            row[7] = border_c
            row[12] = border_c

def modify_blocks(g: List[List[int]]) -> List[List[int]]:
    g = copy.deepcopy(g)
    i = 0
    n_rows = len(g)
    while i < n_rows:
        if not is_block_row(g[i]):
            i += 1
            continue
        border_c = g[i][0]
        interior_c = g[i][1]
        start = i
        i += 1
        while i < n_rows and g[i][0] == border_c and g[i][23] == border_c and g[i][1] == interior_c:
            i += 1
        end = i - 1
        apply_h_pattern(g, start, end, border_c, interior_c)
    return g

def program(g: List[List[int]]) -> List[List[int]]:
    g = fill_background(g)
    g = modify_blocks(g)
    return g
```