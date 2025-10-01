```python
import typing as tp
from collections import Counter
from copy import deepcopy

def get_background(g: tp.List[tp.List[int]]) -> int:
    if not g or not g[0]:
        return 0
    flat = [cell for row in g for cell in row]
    return Counter(flat).most_common(1)[0][0]

def get_fillable(g: tp.List[tp.List[int]], bg: int) -> tp.Set[int]:
    flat = [cell for row in g for cell in row]
    counter = Counter(flat)
    fillable = {bg}
    if 8 in counter and 8 != bg:
        fillable.add(8)
    return fillable

def find_blocks(g: tp.List[tp.List[int]], fillable: tp.Set[int]) -> tp.List[tp.Tuple[int, int, int]]:
    blocks = []
    h = len(g)
    if h < 2:
        return blocks
    w = len(g[0])
    if w < 2:
        return blocks
    for r in range(h - 1):
        for k in range(w - 1):
            c = g[r][k]
            if c != 3 and c not in fillable and g[r][k + 1] == c and g[r + 1][k] == c and g[r + 1][k + 1] == c:
                blocks.append((r, k, c))
    return sorted(blocks, key=lambda x: (x[0], x[1]))

def apply_horizontal(g: tp.List[tp.List[int]], r: int, k: int, c: int, fillable: tp.Set[int], w: int) -> bool:
    changed = False
    for rr in [r, r + 1]:
        if 0 <= rr < len(g):
            # left
            cc = k - 1
            while cc >= 0 and g[rr][cc] in fillable:
                g[rr][cc] = c
                changed = True
                cc -= 1
            # right
            cc = k + 2
            while cc < w and g[rr][cc] in fillable:
                g[rr][cc] = c
                changed = True
                cc += 1
    return changed

def apply_vertical(g: tp.List[tp.List[int]], r: int, k: int, c: int, fillable: tp.Set[int], h: int) -> bool:
    changed = False
    for col in [k, k + 1]:
        # up
        rr = r - 1
        while rr >= 0 and g[rr][col] in fillable:
            g[rr][col] = c
            changed = True
            rr -= 1
        # down
        rr = r + 2
        while rr < h and g[rr][col] in fillable:
            g[rr][col] = c
            changed = True
            rr += 1
    return changed

def apply_diagonal_up_left(g: tp.List[tp.List[int]], r: int, k: int, c: int, fillable: tp.Set[int], w: int) -> bool:
    changed = False
    s = r - k
    rr = r - 1
    while rr >= 0:
        cc = rr - s
        if not (0 <= cc < w) or g[rr][cc] not in fillable:
            break
        g[rr][cc] = c
        changed = True
        rr -= 1
    return changed

def apply_diagonal_up_right(g: tp.List[tp.List[int]], r: int, k: int, c: int, fillable: tp.Set[int], w: int) -> bool:
    changed = False
    s = r + k + 1
    rr = r - 1
    while rr >= 0:
        cc = s - rr
        if not (0 <= cc < w) or g[rr][cc] not in fillable:
            break
        g[rr][cc] = c
        changed = True
        rr -= 1
    return changed

def apply_diagonal_down_left(g: tp.List[tp.List[int]], r: int, k: int, c: int, fillable: tp.Set[int], h: int, w: int) -> bool:
    changed = False
    s = r + 1 + k
    rr = r + 2
    while rr < h:
        cc = s - rr
        if not (0 <= cc < w) or g[rr][cc] not in fillable:
            break
        g[rr][cc] = c
        changed = True
        rr += 1
    return changed

def apply_diagonal_down_right(g: tp.List[tp.List[int]], r: int, k: int, c: int, fillable: tp.Set[int], h: int, w: int) -> bool:
    changed = False
    s = (r + 1) - (k + 1)
    rr = r + 2
    while rr < h:
        cc = rr - s
        if not (0 <= cc < w) or g[rr][cc] not in fillable:
            break
        g[rr][cc] = c
        changed = True
        rr += 1
    return changed

def program(g: tp.List[tp.List[int]]) -> tp.List[tp.List[int]]:
    if not g or not g[0]:
        return g
    h = len(g)
    w = len(g[0])
    bg = get_background(g)
    fillable = get_fillable(g, bg)
    grid = [row[:] for row in g]
    changed = True
    iter_count = 0
    max_iter = h * w
    while changed and iter_count < max_iter:
        iter_count += 1
        blocks = find_blocks(grid, fillable)
        if not blocks:
            break
        temp = [row[:] for row in grid]
        changed = False
        for r, k, c in blocks:
            if apply_horizontal(temp, r, k, c, fillable, w):
                changed = True
            if apply_vertical(temp, r, k, c, fillable, h):
                changed = True
            if apply_diagonal_up_left(temp, r, k, c, fillable, w):
                changed = True
            if apply_diagonal_up_right(temp, r, k, c, fillable, w):
                changed = True
            if apply_diagonal_down_left(temp, r, k, c, fillable, h, w):
                changed = True
            if apply_diagonal_down_right(temp, r, k, c, fillable, h, w):
                changed = True
        grid = temp
    return grid
```