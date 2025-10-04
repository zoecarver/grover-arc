```python
from typing import List

def get_color(typ: int) -> int:
    mapping = {2: 4, 3: 1, 5: 6, 8: 7}
    return mapping.get(typ, 0)

def get_fill(r: int, c: int, typ: int, n: int) -> set:
    if r + 3 >= n or c + 3 >= n or c < 0:
        return set()
    fill = set()
    if typ == 2:
        for dc in range(4):
            fill.add((r, c + dc))
            fill.add((r + 3, c + dc))
        for dr in [1, 2]:
            fill.add((r + dr, c))
            fill.add((r + dr, c + 3))
    elif typ == 3:
        fill.add((r, c + 1))
        fill.add((r, c + 2))
        fill.add((r + 3, c + 1))
        fill.add((r + 3, c + 2))
        for dr in [1, 2]:
            fill.add((r + dr, c))
            fill.add((r + dr, c + 3))
    elif typ == 5:
        for dr in range(2):
            for dc in range(2):
                fill.add((r + dr, c + dc))
        for dr in range(2, 4):
            for dc in range(2, 4):
                fill.add((r + dr, c + dc))
    elif typ == 8:
        fill.add((r, c))
        fill.add((r, c + 3))
        fill.add((r + 3, c))
        fill.add((r + 3, c + 3))
        for dr in [1, 2]:
            fill.add((r + dr, c + 1))
            fill.add((r + dr, c + 2))
    return fill

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    out_grid = [[0] * n for _ in range(n)]
    triggers = []
    for i in range(n):
        for j in range(n):
            t = g[i][j]
            if t in {2, 3, 5, 8}:
                triggers.append((i, j, t))
    if not triggers:
        return out_grid
    triggers.sort(key=lambda x: (x[0], x[1]))
    normal_fills = [get_fill(tr[0], tr[1], tr[2], n) for tr in triggers]
    for ii in range(len(triggers)):
        r, c, typ = triggers[ii]
        normal_fill = normal_fills[ii]
        if not normal_fill:
            continue
        future_conf = []
        for jj in range(ii + 1, len(triggers)):
            if normal_fill & normal_fills[jj]:
                future_conf.append(jj)
        if not future_conf:
            color = get_color(typ)
            for rr, cc in normal_fill:
                out_grid[rr][cc] = color
        else:
            found = False
            for jj in future_conf:
                conf_r = triggers[jj][0]
                delta = conf_r - r
                alt_c = c + delta
                if alt_c < 0 or alt_c + 3 >= n:
                    continue
                alt_fill = get_fill(0, alt_c, typ, n)
                if not alt_fill:
                    continue
                good = True
                for kk in range(len(triggers)):
                    if alt_fill & normal_fills[kk]:
                        good = False
                        break
                if good:
                    color = get_color(typ)
                    for rr, cc in alt_fill:
                        out_grid[rr][cc] = color
                    found = True
                    break
    return out_grid
```