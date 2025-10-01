```python
import typing as tp
from collections import Counter
from copy import deepcopy

def get_background(g: tp.List[tp.List[int]]) -> int:
    if not g or not g[0]:
        return 0
    flat = [cell for row in g for cell in row]
    return Counter(flat).most_common(1)[0][0]

def find_blocks(g: tp.List[tp.List[int]], bg: int) -> tp.List[tp.Tuple[int, int, int]]:
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
            if c != bg and g[r][k + 1] == c and g[r + 1][k] == c and g[r + 1][k + 1] == c:
                blocks.append((r, k, c))
    return blocks

def apply_horizontal(new_g: tp.List[tp.List[int]], r: int, k: int, c: int, bg: int, w: int) -> bool:
    changed = False
    for rr in [r, r + 1]:
        if rr >= len(new_g):
            continue
        # left
        cc = k - 1
        while cc >= 0:
            if new_g[rr][cc] == bg:
                new_g[rr][cc] = c
                changed = True
            elif new_g[rr][cc] != c:
                break
            cc -= 1
        # right
        cc = k + 2
        while cc < w:
            if new_g[rr][cc] == bg:
                new_g[rr][cc] = c
                changed = True
            elif new_g[rr][cc] != c:
                break
            cc += 1
    return changed

def apply_vertical(new_g: tp.List[tp.List[int]], k: int, r: int, c: int, bg: int, h: int) -> bool:
    changed = False
    for col in [k, k + 1]:
        # up
        rr = r - 1
        while rr >= 0:
            if new_g[rr][col] == bg:
                new_g[rr][col] = c
                changed = True
            elif new_g[rr][col] != c:
                break
            rr -= 1
        # down
        rr = r + 2
        while rr < h:
            if new_g[rr][col] == bg:
                new_g[rr][col] = c
                changed = True
            elif new_g[rr][col] != c:
                break
            rr += 1
    return changed

def apply_diagonal_up_left(new_g: tp.List[tp.List[int]], r: int, k: int, c: int, bg: int, h: int, w: int) -> bool:
    changed = False
    d = r - k
    rr = r - 1
    while rr >= 0:
        cc = rr - d
        if not (0 <= cc < w):
            break
        if new_g[rr][cc] == bg:
            new_g[rr][cc] = c
            changed = True
        elif new_g[rr][cc] != c:
            break
        rr -= 1
    return changed

def apply_diagonal_up_right(new_g: tp.List[tp.List[int]], r: int, k: int, c: int, bg: int, h: int, w: int) -> bool:
    changed = False
    s = r + (k + 1)
    rr = r - 1
    while rr >= 0:
        cc = s - rr
        if not (0 <= cc < w):
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
        if not (0 <= cc < w):
            break
        if new_g[rr][cc] == bg:
            new_g[rr][cc] = c
            changed = True
        elif new_g[rr][cc] != c:
            break
        rr += 1
    return changed

def apply_diagonal_down_right(new_g: tp.List[tp.List[int]], r: int, k: int, c: int, bg: int, h: int, w: int) -> bool:
    changed = False
    d = (r + 1) - (k + 1)
    rr = r + 2
    while rr < h:
        cc = rr - d
        if not (0 <= cc < w):
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
    max_iter = h * w
    for _ in range(max_iter):
        blocks = find_blocks(new_g, bg)
        if not blocks:
            break
        changed = False
        blocks.sort(key=lambda x: (x[0], x[1]))
        for r, k, c in blocks:
            if c == 3:
                continue
            ch = apply_horizontal(new_g, r, k, c, bg, w)
            changed = changed or ch
            ch = apply_vertical(new_g, k, r, c, bg, h)
            changed = changed or ch
            ch = apply_diagonal_up_left(new_g, r, k, c, bg, h, w)
            changed = changed or ch
            ch = apply_diagonal_up_right(new_g, r, k, c, bg, h, w)
            changed = changed or ch
            ch = apply_diagonal_down_left(new_g, r, k, c, bg, h, w)
            changed = changed or ch
            ch = apply_diagonal_down_right(new_g, r, k, c, bg, h, w)
            changed = changed or ch
        if not changed:
            break
    return new_g
```