```python
from typing import List
from copy import deepcopy

def get_dimensions(g: List[List[int]]) -> tuple[int, int]:
    if not g:
        return 0, 0
    h = len(g)
    w = len(g[0]) if h > 0 else 0
    return h, w

def fill_horizontal(g: List[List[int]]) -> List[List[int]]:
    g = deepcopy(g)
    h, w = get_dimensions(g)
    for i in range(h):
        j = 0
        while j < w:
            if g[i][j] != 8:
                j += 1
                continue
            start = j
            while j < w and g[i][j] == 8:
                j += 1
            end = j - 1
            l = start - 1
            while l >= 0 and g[i][l] == 8:
                l -= 1
            left_c = g[i][l] if l >= 0 else 0
            r = end + 1
            while r < w and g[i][r] == 8:
                r += 1
            right_c = g[i][r] if r < w else 0
            if left_c == right_c and left_c > 1:
                for k in range(start, end + 1):
                    g[i][k] = left_c
    return g

def fill_vertical(g: List[List[int]]) -> List[List[int]]:
    g = deepcopy(g)
    h, w = get_dimensions(g)
    for j in range(w):
        i = 0
        while i < h:
            if g[i][j] != 8:
                i += 1
                continue
            start = i
            while i < h and g[i][j] == 8:
                i += 1
            end = i - 1
            l = start - 1
            while l >= 0 and g[l][j] == 8:
                l -= 1
            left_c = g[l][j] if l >= 0 else 0
            r = end + 1
            while r < h and g[r][j] == 8:
                r += 1
            right_c = g[r][j] if r < h else 0
            if left_c == right_c and left_c > 1:
                for k in range(start, end + 1):
                    g[k][j] = left_c
    return g

def program(g: List[List[int]]) -> List[List[int]]:
    g = deepcopy(g)
    h, w = get_dimensions(g)
    for _ in range(20):
        g = fill_horizontal(g)
        g = fill_vertical(g)
    return g
```