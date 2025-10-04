```python
from typing import List, Set, Tuple

def get_color(typ: int) -> int:
    if typ == 2:
        return 4
    if typ == 3:
        return 1
    if typ == 5:
        return 6
    if typ == 8:
        return 7
    return 0

def get_fill(r: int, c: int, typ: int, n: int) -> Set[Tuple[int, int]]:
    if r + 3 >= n or c + 3 >= n or c < 0:
        return set()
    fill: Set[Tuple[int, int]] = set()
    if typ == 2:
        for dc in range(4):
            fill.add((r, c + dc))
            fill.add((r + 3, c + dc))
        for dr in (1, 2):
            fill.add((r + dr, c))
            fill.add((r + dr, c + 3))
    elif typ == 3:
        fill.add((r, c + 1))
        fill.add((r, c + 2))
        fill.add((r + 3, c + 1))
        fill.add((r + 3, c + 2))
        for dr in (1, 2):
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
        for dr in (1, 2):
            fill.add((r + dr, c + 1))
            fill.add((r + dr, c + 2))
    return fill

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    triggers: List[Tuple[int, int, int]] = []
    for i in range(n):
        for j in range(n):
            val = g[i][j]
            if val in (2, 3, 5, 8):
                triggers.append((i, j, val))
    triggers.sort(key=lambda x: (x[0], x[1]))
    out_grid: List[List[int]] = [[0] * n for _ in range(n)]
    for idx in range(len(triggers)):
        r, c, typ = triggers[idx]
        color = get_color(typ)
        normal_fill = get_fill(r, c, typ, n)
        if not normal_fill:
            continue
        intersects_placed = any(out_grid[rr][cc] != 0 for rr, cc in normal_fill)
        conflicting_deltas: set[int] = set()
        for j in range(idx + 1, len(triggers)):
            fr, fc, ftyp = triggers[j]
            f_fill = get_fill(fr, fc, ftyp, n)
            if normal_fill & f_fill:
                delta = fr - r
                conflicting_deltas.add(delta)
        if not intersects_placed and not conflicting_deltas:
            for rr, cc in normal_fill:
                out_grid[rr][cc] = color
            continue
        placed_this = False
        for delta in sorted(conflicting_deltas):
            sc = c + delta
            if sc < 0 or sc + 3 >= n:
                continue
            shifted_fill = get_fill(r, sc, typ, n)
            if not shifted_fill:
                continue
            s_intersects_placed = any(out_grid[rr][cc] != 0 for rr, cc in shifted_fill)
            s_intersects_future = any(
                get_fill(triggers[j][0], triggers[j][1], triggers[j][2], n) & shifted_fill
                for j in range(idx + 1, len(triggers))
            )
            if not s_intersects_placed and not s_intersects_future:
                for rr, cc in shifted_fill:
                    out_grid[rr][cc] = color
                placed_this = True
                break
    return out_grid
```