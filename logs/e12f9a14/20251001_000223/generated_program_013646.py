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
            if c != bg and c != 3 and g[r][k + 1] == c and g[r + 1][k] == c and g[r + 1][k + 1] == c:
                blocks.append((r, k, c))
    return sorted(blocks, key=lambda x: (x[0], x[1]))

def apply_horizontal(temp_g: tp.List[tp.List[int]], r: int, k: int, c: int, bg: int, h: int, w: int):
    for rr in (r, r + 1):
        if 0 <= rr < h:
            apply_horizontal_left(temp_g, rr, k, c, bg, w)
            apply_horizontal_right(temp_g, rr, k, c, bg, h, w)

def apply_horizontal_left(temp_g: tp.List[tp.List[int]], rr: int, k: int, c: int, bg: int, w: int):
    cc = k - 1
    last_filled = None
    while cc >= 0:
        if temp_g[rr][cc] != bg and temp_g[rr][cc] != c:
            break
        next_cc = cc - 1
        is_end = next_cc < 0
        is_blocked_next = not is_end and (temp_g[rr][next_cc] != bg and temp_g[rr][next_cc] != c)
        if is_end or is_blocked_next:
            if is_end:
                if temp_g[rr][cc] == bg:
                    temp_g[rr][cc] = c
                    last_filled = cc
            else:
                if last_filled is not None:
                    apply_down_left_from_point(temp_g, rr, last_filled, c, bg, len(temp_g), w)
            break
        if temp_g[rr][cc] == bg:
            temp_g[rr][cc] = c
            last_filled = cc
        cc -= 1

def apply_horizontal_right(temp_g: tp.List[tp.List[int]], rr: int, k: int, c: int, bg: int, h: int, w: int):
    cc = k + 2
    last_filled = None
    while cc < w:
        if temp_g[rr][cc] != bg and temp_g[rr][cc] != c:
            break
        next_cc = cc + 1
        is_end = next_cc >= w
        is_blocked_next = not is_end and (temp_g[rr][next_cc] != bg and temp_g[rr][next_cc] != c)
        if is_end or is_blocked_next:
            if is_end:
                if temp_g[rr][cc] == bg:
                    temp_g[rr][cc] = c
                    last_filled = cc
            else:
                if last_filled is not None:
                    apply_down_right_from_point(temp_g, rr, last_filled, c, bg, h, w)
            break
        if temp_g[rr][cc] == bg:
            temp_g[rr][cc] = c
            last_filled = cc
        cc += 1

def apply_vertical(temp_g: tp.List[tp.List[int]], r: int, k: int, c: int, bg: int, h: int):
    for col in (k, k + 1):
        # up
        rr = r - 1
        while rr >= 0:
            if temp_g[rr][col] == bg:
                temp_g[rr][col] = c
            elif temp_g[rr][col] != c:
                break
            rr -= 1
        # down
        rr = r + 2
        while rr < h:
            if temp_g[rr][col] == bg:
                temp_g[rr][col] = c
            elif temp_g[rr][col] != c:
                break
            rr += 1

def apply_diag_up_right(temp_g: tp.List[tp.List[int]], r: int, k: int, c: int, bg: int, h: int, w: int):
    s = r + k + 1
    rr = r - 1
    while rr >= 0:
        cc = s - rr
        if cc < 0 or cc >= w:
            break
        if temp_g[rr][cc] == bg:
            temp_g[rr][cc] = c
        elif temp_g[rr][cc] != c:
            break
        rr -= 1

def apply_diag_down_left(temp_g: tp.List[tp.List[int]], r: int, k: int, c: int, bg: int, h: int, w: int):
    s = r + k + 1
    rr = r + 2
    while rr < h:
        cc = s - rr
        if cc < 0 or cc >= w:
            break
        if temp_g[rr][cc] == bg:
            temp_g[rr][cc] = c
        elif temp_g[rr][cc] != c:
            break
        rr += 1

def apply_diag_up_left(temp_g: tp.List[tp.List[int]], r: int, k: int, c: int, bg: int, h: int, w: int):
    d = r - k
    rr = r - 1
    while rr >= 0:
        cc = rr - d
        if cc < 0 or cc >= w:
            break
        if temp_g[rr][cc] == bg:
            temp_g[rr][cc] = c
        elif temp_g[rr][cc] != c:
            break
        rr -= 1

def apply_diag_down_right(temp_g: tp.List[tp.List[int]], r: int, k: int, c: int, bg: int, h: int, w: int):
    d = r - k
    rr = r + 2
    while rr < h:
        cc = rr - d
        if cc < 0 or cc >= w:
            break
        if temp_g[rr][cc] == bg:
            temp_g[rr][cc] = c
        elif temp_g[rr][cc] != c:
            break
        rr += 1

def apply_down_right_from_point(temp_g: tp.List[tp.List[int]], rr: int, cc: int, c: int, bg: int, h: int, w: int):
    current_rr = rr + 1
    current_cc = cc + 1
    while current_rr < h and current_cc < w:
        if temp_g[current_rr][current_cc] != bg and temp_g[current_rr][current_cc] != c:
            break
        if temp_g[current_rr][current_cc] == bg:
            temp_g[current_rr][current_cc] = c
        current_rr += 1
        current_cc += 1

def apply_down_left_from_point(temp_g: tp.List[tp.List[int]], rr: int, cc: int, c: int, bg: int, h: int, w: int):
    current_rr = rr + 1
    current_cc = cc - 1
    while current_rr < h and current_cc >= 0:
        if temp_g[current_rr][current_cc] != bg and temp_g[current_rr][current_cc] != c:
            break
        if temp_g[current_rr][current_cc] == bg:
            temp_g[current_rr][current_cc] = c
        current_rr += 1
        current_cc -= 1

def program(g: tp.List[tp.List[int]]) -> tp.List[tp.List[int]]:
    if not g or not g[0]:
        return g
    h = len(g)
    w = len(g[0])
    bg = get_background(g)
    new_g = [row[:] for row in g]
    while True:
        old_g = deepcopy(new_g)
        blocks = find_blocks(new_g, bg)
        for r, k, c in blocks:
            apply_horizontal(new_g, r, k, c, bg, h, w)
            apply_vertical(new_g, r, k, c, bg, h)
            apply_diag_up_right(new_g, r, k, c, bg, h, w)
            apply_diag_down_left(new_g, r, k, c, bg, h, w)
            apply_diag_up_left(new_g, r, k, c, bg, h, w)
            apply_diag_down_right(new_g, r, k, c, bg, h, w)
        if new_g == old_g:
            break
    return new_g
```