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
            if (c != bg and
                g[r][k + 1] == c and
                g[r + 1][k] == c and
                g[r + 1][k + 1] == c):
                blocks.append((r, k, c))
    return blocks

def apply_horizontal_bottom(new_g: tp.List[tp.List[int]], blocks: tp.List[tp.Tuple[int, int, int]], bg: int, w: int) -> None:
    for r, k, c in blocks:
        rr = r + 1  # bottom row of block
        if rr >= len(new_g):
            continue
        # right fill in bottom row if open right
        if k + 2 < w and new_g[rr][k + 1 + 1] == bg:
            for cc in range(k + 2, w):
                if new_g[rr][cc] != bg:
                    break
                new_g[rr][cc] = c
        # left fill in bottom row if open left
        if k - 1 >= 0 and new_g[rr][k - 1] == bg:
            for cc in range(k - 1, -1, -1):
                if new_g[rr][cc] != bg:
                    break
                new_g[rr][cc] = c

def apply_vertical_ups(new_g: tp.List[tp.List[int]], blocks: tp.List[tp.Tuple[int, int, int]], bg: int) -> None:
    h = len(new_g)
    for r, k, c in blocks:
        if k + 1 >= len(new_g[0]):
            continue
        # vertical up from left column k starting from row r
        for rr in range(r - 1, -1, -1):
            if new_g[rr][k] != bg:
                break
            new_g[rr][k] = c
        # vertical up from right column k+1 starting from row r
        for rr in range(r - 1, -1, -1):
            if new_g[rr][k + 1] != bg:
                break
            new_g[rr][k + 1] = c

def apply_diagonal_up_right(new_g: tp.List[tp.List[int]], blocks: tp.List[tp.Tuple[int, int, int]], bg: int, w: int) -> None:
    for r, k, c in blocks:
        if k + 1 >= w:
            continue
        s = r + k + 1
        for rr in range(r - 1, -1, -1):
            cc = s - rr
            if not (0 <= cc < w) or new_g[rr][cc] != bg:
                break
            new_g[rr][cc] = c

def apply_diagonal_down_left(new_g: tp.List[tp.List[int]], blocks: tp.List[tp.Tuple[int, int, int]], bg: int, h: int, w: int) -> None:
    for r, k, c in blocks:
        if r + 1 >= h or k >= w:
            continue
        s = (r + 1) + k
        for rr in range(r + 2, h):
            cc = s - rr
            if not (0 <= cc < w) or new_g[rr][cc] != bg:
                break
            new_g[rr][cc] = c

def program(g: tp.List[tp.List[int]]) -> tp.List[tp.List[int]]:
    if not g or not g[0]:
        return g
    h = len(g)
    w = len(g[0])
    bg = get_background(g)
    new_g = [row[:] for row in g]
    blocks = find_blocks(g, bg)
    apply_horizontal_bottom(new_g, blocks, bg, w)
    apply_vertical_ups(new_g, blocks, bg)
    apply_diagonal_up_right(new_g, blocks, bg, w)
    apply_diagonal_down_left(new_g, blocks, bg, h, w)
    return new_g
```