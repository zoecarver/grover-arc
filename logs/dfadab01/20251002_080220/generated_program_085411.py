```python
from typing import List, Set, Tuple

def get_color(typ: int) -> int:
    mapping = {2: 4, 3: 1, 5: 6, 8: 7}
    return mapping.get(typ, 0)

def get_fill(r: int, c: int, typ: int, n: int) -> Set[Tuple[int, int]]:
    if c < 0:
        return set()
    fill: Set[Tuple[int, int]] = set()
    positions: List[Tuple[int, int]] = []
    if typ == 2:
        for dc in range(4):
            positions.append((r, c + dc))
            positions.append((r + 3, c + dc))
        for dr in (1, 2):
            positions.append((r + dr, c))
            positions.append((r + dr, c + 3))
    elif typ == 3:
        positions.append((r, c + 1))
        positions.append((r, c + 2))
        positions.append((r + 3, c + 1))
        positions.append((r + 3, c + 2))
        for dr in (1, 2):
            positions.append((r + dr, c))
            positions.append((r + dr, c + 3))
    elif typ == 5:
        for dr in range(2):
            for dc in range(2):
                positions.append((r + dr, c + dc))
        for dr in range(2, 4):
            for dc in range(2, 4):
                positions.append((r + dr, c + dc))
    elif typ == 8:
        positions.append((r, c))
        positions.append((r, c + 3))
        positions.append((r + 3, c))
        positions.append((r + 3, c + 3))
        for dr in (1, 2):
            positions.append((r + dr, c + 1))
            positions.append((r + dr, c + 2))
    for rr, cc in positions:
        if 0 <= rr < n and 0 <= cc < n:
            fill.add((rr, cc))
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