```python
import typing as tp
from collections import Counter
import copy

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
            if c != bg and c != 3 and g[r][k + 1] == c and g[r + 1][k] == c and g[r + 1][k + 1] == c:
                blocks.append((r, k, c))
    return sorted(blocks, key=lambda x: (x[0], x[1]))  # sort by row then col

def apply_horizontal(new_g: tp.List[tp.List[int]], rr: int, k: int, c: int, bg: int, w: int) -> bool:
    changed = False
    # left from k-1
    cc = k - 1
    while cc >= 0:
        cell = new_g[rr][cc]
        if cell == bg:
            new_g[rr][cc] = c
            changed = True
        elif cell != c and cell != 3:
            break
        cc -= 1
    # right from k+2
    cc = k + 2
    while cc < w:
        cell = new_g[rr][cc]
        if cell == bg:
            new_g[rr][cc] = c
            changed = True
        elif cell != c and cell != 3:
            break
        cc += 1
    return changed

def apply_vertical(new_g: tp.List[tp.List[int]], cc: int, r: int, c: int, bg: int, h: int) -> bool:
    changed = False
    # up from r-1
    rr = r - 1
    while rr >= 0:
        cell = new_g[rr][cc]
        if cell == bg:
            new_g[rr][cc] = c
            changed = True
        elif cell != c and cell != 3:
            break
        rr -= 1
    # down from r+2
    rr = r + 2
    while rr < h:
        cell = new_g[rr][cc]
        if cell == bg:
            new_g[rr][cc] = c
            changed = True
        elif cell != c and cell != 3:
            break
        rr += 1
    return changed

def apply_diagonal_up_left(new_g: tp.List[tp.List[int]], start_r: int, start_c: int, c: int, bg: int, h: int, w: int) -> bool:
    changed = False
    rr = start_r - 1
    cc = start_c - 1
    while 0 <= rr < h and 0 <= cc < w:
        cell = new_g[rr][cc]
        if cell == bg:
            new_g[rr][cc] = c
            changed = True
        elif cell != c and cell != 3:
            break
        rr -= 1
        cc -= 1
    return changed

def apply_diagonal_up_right(new_g: tp.List[tp.List[int]], start_r: int, start_c: int, c: int, bg: int, h: int, w: int) -> bool:
    changed = False
    rr = start_r - 1
    cc = start_c + 1
    while 0 <= rr < h and 0 <= cc < w:
        cell = new_g[rr][cc]
        if cell == bg:
            new_g[rr][cc] = c
            changed = True
        elif cell != c and cell != 3:
            break
        rr -= 1
        cc += 1
    return changed

def apply_diagonal_down_left(new_g: tp.List[tp.List[int]], start_r: int, start_c: int, c: int, bg: int, h: int, w: int) -> bool:
    changed = False
    rr = start_r + 1
    cc = start_c - 1
    while 0 <= rr < h and 0 <= cc < w:
        cell = new_g[rr][cc]
        if cell == bg:
            new_g[rr][cc] = c
            changed = True
        elif cell != c and cell != 3:
            break
        rr += 1
        cc -= 1
    return changed

def apply_diagonal_down_right(new_g: tp.List[tp.List[int]], start_r: int, start_c: int, c: int, bg: int, h: int, w: int) -> bool:
    changed = False
    rr = start_r + 1
    cc = start_c + 1
    while 0 <= rr < h and 0 <= cc < w:
        cell = new_g[rr][cc]
        if cell == bg:
            new_g[rr][cc] = c
            changed = True
        elif cell != c and cell != 3:
            break
        rr += 1
        cc += 1
    return changed

def program(g: tp.List[tp.List[int]]) -> tp.List[tp.List[int]]:
    if not g or not g[0]:
        return g
    h = len(g)
    w = len(g[0])
    bg = get_background(g)
    new_g = copy.deepcopy(g)
    max_iters = h * w
    for _ in range(max_iters):
        blocks = find_blocks(new_g, bg)
        if not blocks:
            break
        changed = False
        for r, k, c in blocks:
            # horizontal
            changed |= apply_horizontal(new_g, r, k, c, bg, w)
            changed |= apply_horizontal(new_g, r + 1, k, c, bg, w)
            # vertical
            changed |= apply_vertical(new_g, k, r, c, bg, h)
            changed |= apply_vertical(new_g, k + 1, r, c, bg, h)
            # diagonals from corners
            changed |= apply_diagonal_up_left(new_g, r, k, c, bg, h, w)
            changed |= apply_diagonal_up_right(new_g, r, k + 1, c, bg, h, w)
            changed |= apply_diagonal_down_left(new_g, r + 1, k, c, bg, h, w)
            changed |= apply_diagonal_down_right(new_g, r + 1, k + 1, c, bg, h, w)
        if not changed:
            break
    return new_g
```