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
    w = len(g[0]) if h > 0 else 0
    for r in range(h - 1):
        for k in range(w - 1):
            c = g[r][k]
            if c != bg and c != 3 and g[r][k + 1] == c and g[r + 1][k] == c and g[r + 1][k + 1] == c:
                blocks.append((r, k, c))
    return sorted(blocks, key=lambda x: (x[0], x[1]))

def apply_horizontal(temp_g: tp.List[tp.List[int]], r: int, k: int, c: int, bg: int, w: int) -> None:
    for rr in [r, r + 1]:
        if 0 <= rr < len(temp_g):
            count = 0
            cc = k - 1
            while count < 4 and 0 <= cc < w and temp_g[rr][cc] == bg:
                temp_g[rr][cc] = c
                count += 1
                cc -= 1
            count = 0
            cc = k + 2
            while count < 4 and cc < w and temp_g[rr][cc] == bg:
                temp_g[rr][cc] = c
                count += 1
                cc += 1

def apply_vertical(temp_g: tp.List[tp.List[int]], r: int, k: int, c: int, bg: int, h: int) -> None:
    for col in [k, k + 1]:
        rr = r - 1
        while 0 <= rr < h and (temp_g[rr][col] == bg or temp_g[rr][col] == 3):
            temp_g[rr][col] = c
            rr -= 1
        rr = r + 2
        while rr < h and temp_g[rr][col] == bg:
            temp_g[rr][col] = c
            rr += 1

def apply_up_left(temp_g: tp.List[tp.List[int]], r: int, k: int, c: int, bg: int, w: int) -> None:
    s = r - k
    rr = r - 1
    while 0 <= rr < len(temp_g):
        cc = rr - s
        if not (0 <= cc < w) or temp_g[rr][cc] != bg:
            break
        temp_g[rr][cc] = c
        rr -= 1

def apply_up_right(temp_g: tp.List[tp.List[int]], r: int, k: int, c: int, bg: int, w: int) -> None:
    s = r + k + 1
    rr = r - 1
    while 0 <= rr < len(temp_g):
        cc = s - rr
        if not (0 <= cc < w) or temp_g[rr][cc] != bg:
            break
        temp_g[rr][cc] = c
        rr -= 1

def apply_down_left(temp_g: tp.List[tp.List[int]], r: int, k: int, c: int, bg: int, h: int, w: int) -> None:
    s = r + k + 1
    rr = r + 2
    while rr < h:
        cc = s - rr
        if not (0 <= cc < w) or temp_g[rr][cc] != bg:
            break
        temp_g[rr][cc] = c
        rr += 1

def apply_down_right(temp_g: tp.List[tp.List[int]], r: int, k: int, c: int, bg: int, h: int, w: int) -> None:
    s = r - k
    rr = r + 2
    while rr < h:
        cc = rr - s
        if not (0 <= cc < w) or temp_g[rr][cc] != bg:
            break
        temp_g[rr][cc] = c
        rr += 1

def program(g: tp.List[tp.List[int]]) -> tp.List[tp.List[int]]:
    if not g or not g[0]:
        return g
    h = len(g)
    w = len(g[0])
    bg = get_background(g)
    iter_count = 0
    max_iter = h * w
    while iter_count < max_iter:
        iter_count += 1
        blocks = find_blocks(g, bg)
        if not blocks:
            break
        temp_g = [row[:] for row in g]
        for r, k, c in blocks:
            apply_horizontal(temp_g, r, k, c, bg, w)
            apply_vertical(temp_g, r, k, c, bg, h)
            apply_up_left(temp_g, r, k, c, bg, w)
            apply_up_right(temp_g, r, k, c, bg, w)
            apply_down_left(temp_g, r, k, c, bg, h, w)
            apply_down_right(temp_g, r, k, c, bg, h, w)
            # special down-right from right h end on top row if filled 4
            rr = r
            if 0 <= rr < h:
                start_cc = k + 2
                filled_4 = start_cc + 4 <= w and all(temp_g[rr][start_cc + i] == c for i in range(4))
                if filled_4:
                    curr_r = rr + 1
                    curr_c = start_cc + 4
                    while curr_r < h and 0 <= curr_c < w and temp_g[curr_r][curr_c] == bg:
                        temp_g[curr_r][curr_c] = c
                        curr_r += 1
                        curr_c += 1
        g = temp_g
    return g
```