```python
from typing import List

def prune_small_components(g: List[List[int]]) -> List[List[int]]:
    h = len(g)
    if h == 0:
        return []
    w = len(g[0])
    out = [row[:] for row in g]
    dirs4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(h):
        for j in range(w):
            if g[i][j] == 1:
                n = sum(1 for di, dj in dirs4 if 0 <= i + di < h and 0 <= j + dj < w and g[i + di][j + dj] == 1)
                if n < 2:
                    out[i][j] = 0
    return out

def set_internal_boundaries(out: List[List[int]], base: List[List[int]]) -> List[List[int]]:
    h = len(base)
    if h == 0:
        return out
    w = len(base[0])
    dirs4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    dirs8 = [(di, dj) for di in [-1, 0, 1] for dj in [-1, 0, 1] if not (di == 0 and dj == 0)]
    for i in range(h):
        for j in range(w):
            if base[i][j] == 1:
                has_qualifying_zero = False
                for di, dj in dirs8:
                    ni = i + di
                    nj = j + dj
                    if 0 <= ni < h and 0 <= nj < w and base[ni][nj] == 0:
                        n1 = sum(1 for ddi, ddj in dirs4 if 0 <= ni + ddi < h and 0 <= nj + ddj < w and base[ni + ddi][nj + ddj] == 1)
                        if n1 >= 3:
                            has_qualifying_zero = True
                            break
                if has_qualifying_zero:
                    out[i][j] = 7
    return out

def fill_open_pockets(out: List[List[int]], base: List[List[int]]) -> List[List[int]]:
    h = len(base)
    if h == 0:
        return out
    w = len(base[0])
    dirs4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(h):
        for j in range(w):
            if base[i][j] == 0:
                n1 = sum(1 for di, dj in dirs4 if 0 <= i + di < h and 0 <= j + dj < w and base[i + di][j + dj] == 1)
                if n1 == 3:
                    open_di = open_dj = None
                    for di, dj in dirs4:
                        ni = i + di
                        nj = j + dj
                        if not (0 <= ni < h and 0 <= nj < w and base[ni][nj] == 1):
                            open_di = di
                            open_dj = dj
                            break
                    if open_dj == 0 and open_di is not None:
                        ni = i + open_di
                        if 0 <= ni < h:
                            for djj in [-1, 0, 1]:
                                njj = j + djj
                                if 0 <= njj < w:
                                    out[ni][njj] = 7
                        if open_di == 1 and i >= h // 2:
                            out[i][j] = 7
    return out

def program(g: List[List[int]]) -> List[List[int]]:
    pruned = prune_small_components(g)
    out = [row[:] for row in pruned]
    out = fill_open_pockets(out, pruned)
    out = set_internal_boundaries(out, pruned)
    return out
```