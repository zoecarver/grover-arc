```python
from typing import List

def expand_green(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return g
    r, c = len(g), len(g[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    changed = True
    while changed:
        changed = False
        new_g = [row[:] for row in g]
        for i in range(r):
            for j in range(c):
                if g[i][j] == 1:
                    adjacent_green = any(
                        0 <= i + di < r and 0 <= j + dj < c and g[i + di][j + dj] == 3
                        for di, dj in directions
                    )
                    if adjacent_green:
                        new_g[i][j] = 3
                        changed = True
        g = new_g
    return g

def expand_other(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return g
    r, c = len(g), len(g[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    changed = True
    while changed:
        changed = False
        new_g = [row[:] for row in g]
        for i in range(r):
            for j in range(c):
                if g[i][j] == 1:
                    color = 0
                    for di, dj in directions:
                        ni, nj = i + di, j + dj
                        if 0 <= ni < r and 0 <= nj < c and g[ni][nj] != 1:
                            color = g[ni][nj]
                            break
                    new_g[i][j] = color
                    if new_g[i][j] != 1:
                        changed = True
        g = new_g
    return g

def transpose(g: List[List[int]]) -> List[List[int]]:
    return [list(row) for row in zip(*g)]

def program(g: List[List[int]]) -> List[List[int]]:
    g = expand_green(g)
    g = expand_other(g)
    return transpose(g)
```