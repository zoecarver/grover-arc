```python
from typing import List
from copy import deepcopy

def make_grid_copy(g: List[List[int]]) -> List[List[int]]:
    return deepcopy(g)

def reflect_horizontal(g: List[List[int]]) -> List[List[int]]:
    g = make_grid_copy(g)
    for r in range(27):
        if r == 13:
            continue
        for c in range(13):
            if g[r][c] != 4:
                c2 = 26 - c
                if g[r][c2] == 4:
                    g[r][c2] = g[r][c]
            if g[r][26 - c] != 4:
                c2 = 26 - c
                if g[r][c] == 4:
                    g[r][c] = g[r][c2]
    return g

def reflect_vertical(g: List[List[int]]) -> List[List[int]]:
    g = make_grid_copy(g)
    for c in range(27):
        if c == 13:
            continue
        for r in range(13):
            if g[r][c] != 4:
                r2 = 26 - r
                if g[r2][c] == 4:
                    g[r2][c] = g[r][c]
            if g[26 - r][c] != 4:
                r2 = 26 - r
                if g[r][c] == 4:
                    g[r][c] = g[r2][c]
    return g

def reflect_180(g: List[List[int]]) -> List[List[int]]:
    g = make_grid_copy(g)
    for r in range(27):
        if r == 13:
            continue
        r2 = 26 - r
        for c in range(27):
            if c == 13:
                continue
            c2 = 26 - c
            if g[r][c] != 4 and g[r2][c2] == 4:
                g[r2][c2] = g[r][c]
            if g[r2][c2] != 4 and g[r][c] == 4:
                g[r][c] = g[r2][c2]
    return g

def program(g: List[List[int]]) -> List[List[int]]:
    g = make_grid_copy(g)
    for _ in range(10):
        g = reflect_horizontal(g)
        g = reflect_vertical(g)
        g = reflect_180(g)
    return g
```