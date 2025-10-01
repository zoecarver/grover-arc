```python
from typing import List
from collections import Counter

def get_background(g: List[List[int]]) -> int:
    if not g or not g[0]:
        return 0
    flat = [cell for row in g for cell in row]
    return Counter(flat).most_common(1)[0][0]

def find_blocks(g: List[List[int]], bg: int) -> List[tuple[int, int, int]]:
    blocks = []
    h = len(g)
    w = len(g[0]) if h > 0 else 0
    for r in range(h - 1):
        for k in range(w - 1):
            c = g[r][k]
            if c != bg and c != 3 and g[r][k + 1] == c and g[r + 1][k] == c and g[r + 1][k + 1] == c:
                blocks.append((r, k, c))
    return sorted(blocks, key=lambda x: (x[0], x[1]))

def apply_horizontal(temp_g: List[List[int]], r: int, k: int, c: int, bg: int, w: int) -> None:
    for rr in [r, r + 1]:
        if 0 <= rr < len(temp_g):
            cc = k - 1
            while 0 <= cc < w and temp_g[rr][cc] == bg:
                temp_g[rr][cc] = c
                cc -= 1
            cc = k + 2
            while cc < w and temp_g[rr][cc] == bg:
                temp_g[rr][cc] = c
                cc += 1

def apply_vertical(temp_g: List[List[int]], r: int, k: int, c: int, bg: int, h: int) -> None:
    for col in [k, k + 1]:
        rr = r - 1
        while 0 <= rr < h and temp_g[rr][col] == bg:
            temp_g[rr][col] = c
            rr -= 1
        rr = r + 2
        while rr < h and temp_g[rr][col] == bg:
            temp_g[rr][col] = c
            rr += 1

def apply_diagonal_up_right(temp_g: List[List[int]], r: int, k: int, c: int, bg: int, w: int) -> None:
    s = r + k + 1
    rr = r - 1
    while 0 <= rr < len(temp_g):
        cc = s - rr
        if not (0 <= cc < w) or temp_g[rr][cc] != bg:
            break
        temp_g[rr][cc] = c
        rr -= 1

def apply_diagonal_down_left(temp_g: List[List[int]], r: int, k: int, c: int, bg: int, h: int, w: int) -> None:
    s = (r + 1) + k
    rr = r + 2
    while rr < h:
        cc = s - rr
        if not (0 <= cc < w) or temp_g[rr][cc] != bg:
            break
        temp_g[rr][cc] = c
        rr += 1

def apply_diagonal_up_left(temp_g: List[List[int]], r: int, k: int, c: int, bg: int, w: int) -> None:
    s = r - k
    rr = r - 1
    while 0 <= rr < len(temp_g):
        cc = rr - s
        if not (0 <= cc < w) or temp_g[rr][cc] != bg:
            break
        temp_g[rr][cc] = c
        rr -= 1

def apply_diagonal_down_right(temp_g: List[List[int]], r: int, k: int, c: int, bg: int, h: int, w: int) -> None:
    s = (r + 1) - (k + 1)
    rr = r + 2
    while rr < h:
        cc = rr - s
        if not (0 <= cc < w) or temp_g[rr][cc] != bg:
            break
        temp_g[rr][cc] = c
        rr += 1

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return g
    h = len(g)
    w = len(g[0])
    bg = get_background(g)
    new_g = [row[:] for row in g]
    iter_count = 0
    max_iter = h * w
    while iter_count < max_iter:
        blocks = find_blocks(new_g, bg)
        if not blocks:
            break
        temp_g = [row[:] for row in new_g]
        for r, k, c in blocks:
            apply_horizontal(temp_g, r, k, c, bg, w)
            apply_vertical(temp_g, r, k, c, bg, h)
            apply_diagonal_up_right(temp_g, r, k, c, bg, w)
            apply_diagonal_down_left(temp_g, r, k, c, bg, h, w)
            apply_diagonal_up_left(temp_g, r, k, c, bg, w)
            apply_diagonal_down_right(temp_g, r, k, c, bg, h, w)
        changed = False
        for i in range(h):
            if temp_g[i] != new_g[i]:
                changed = True
                new_g[i] = temp_g[i][:]
                break
        if not changed:
            break
        iter_count += 1
    return new_g
```