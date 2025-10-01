```python
import typing as tp
from collections import Counter

def get_background(g: tp.List[tp.List[int]]) -> int:
    if not g or not g[0]:
        return 0
    flat = [cell for row in g for cell in row]
    return Counter(flat).most_common(1)[0][0]

def find_blocks(g: tp.List[tp.List[int]], bg: int) -> tp.List[tp.Tuple[int, int, int]]:
    blocks = []
    h = len(g)
    w = len(g[0])
    for r in range(h - 1):
        for k in range(w - 1):
            c = g[r][k]
            if c != bg and g[r][k + 1] == c and g[r + 1][k] == c and g[r + 1][k + 1] == c:
                blocks.append((r, k, c))
    return blocks

def apply_horizontal(new_g: tp.List[tp.List[int]], rr: int, k: int, c: int, bg: int, w: int) -> bool:
    changed = False
    # right
    cc = k + 2
    while cc < w:
        if new_g[rr][cc] == bg:
            new_g[rr][cc] = c
            changed = True
        elif new_g[rr][cc] != c:
            break
        cc += 1
    # left
    cc = k - 1
    while cc >= 0:
        if new_g[rr][cc] == bg:
            new_g[rr][cc] = c
            changed = True
        elif new_g[rr][cc] != c:
            break
        cc -= 1
    return changed

def apply_vertical(new_g: tp.List[tp.List[int]], col: int, r: int, c: int, bg: int, h: int, up: bool) -> bool:
    changed = False
    if up:
        step = -1
        start = r - 1
        stop = -1
    else:
        step = 1
        start = r + 2
        stop = h
    rr = start
    while (up and rr >= 0) or (not up and rr < h):
        if new_g[rr][col] == bg:
            new_g[rr][col] = c
            changed = True
        elif new_g[rr][col] != c:
            break
        rr += step
    return changed

def apply_diagonal_up_right(new_g: tp.List[tp.List[int]], r: int, k: int, c: int, bg: int, w: int) -> bool:
    changed = False
    s = r + k + 1
    rr = r - 1
    while rr >= 0:
        cc = s - rr
        if cc >= w:
            break
        if new_g[rr][cc] == bg:
            new_g[rr][cc] = c
            changed = True
        elif new_g[rr][cc] != c:
            break
        rr -= 1
    return changed

def apply_diagonal_down_left(new_g: tp.List[tp.List[int]], r: int, k: int, c: int, bg: int, h: int, w: int) -> bool:
    changed = False
    s = (r + 1) + k
    rr = r + 2
    while rr < h:
        cc = s - rr
        if cc < 0:
            break
        if new_g[rr][cc] == bg:
            new_g[rr][cc] = c
            changed = True
        elif new_g[rr][cc] != c:
            break
        rr += 1
    return changed

def program(g: tp.List[tp.List[int]]) -> tp.List[tp.List[int]]:
    if not g or not g[0]:
        return g
    h = len(g)
    w = len(g[0])
    bg = get_background(g)
    new_g = [row[:] for row in g]
    changed = True
    while changed:
        changed = False
        blocks = sorted(find_blocks(new_g, bg), key=lambda b: b[0])
        for r, k, c in blocks:
            if apply_horizontal(new_g, r, k, c, bg, w):
                changed = True
            if apply_horizontal(new_g, r + 1, k, c, bg, w):
                changed = True
            if apply_vertical(new_g, k, r, c, bg, h, True):
                changed = True
            if apply_vertical(new_g, k + 1, r, c, bg, h, True):
                changed = True
            if apply_vertical(new_g, k, r, c, bg, h, False):
                changed = True
            if apply_vertical(new_g, k + 1, r, c, bg, h, False):
                changed = True
            if apply_diagonal_up_right(new_g, r, k, c, bg, w):
                changed = True
            if apply_diagonal_down_left(new_g, r, k, c, bg, h, w):
                changed = True
    return new_g
```