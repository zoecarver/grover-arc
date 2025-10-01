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

def apply_horizontal_bottom(new_g: tp.List[tp.List[int]], blocks: tp.List[tp.Tuple[int, int, int]], bg: int, w: int) -> None:
    for r, k, c in blocks:
        rr = r + 1
        if rr >= len(new_g):
            continue
        # left fill in bottom row
        pos = k - 1
        while pos >= 0 and new_g[rr][pos] == bg:
            new_g[rr][pos] = c
            pos -= 1
        # right fill in bottom row
        pos = k + 2
        while pos < w and new_g[rr][pos] == bg:
            new_g[rr][pos] = c
            pos += 1

def apply_horizontal_top(new_g: tp.List[tp.List[int]], blocks: tp.List[tp.Tuple[int, int, int]], bg: int, w: int) -> None:
    for r, k, c in blocks:
        rr = r
        # left fill in top row
        pos = k - 1
        while pos >= 0 and new_g[rr][pos] == bg:
            new_g[rr][pos] = c
            pos -= 1
        # right fill in top row
        pos = k + 2
        while pos < w and new_g[rr][pos] == bg:
            new_g[rr][pos] = c
            pos += 1

def apply_vertical_ups(new_g: tp.List[tp.List[int]], blocks: tp.List[tp.Tuple[int, int, int]], bg: int) -> None:
    for r, k, c in blocks:
        # left column up from top of block
        rr = r - 1
        while rr >= 0 and new_g[rr][k] == bg:
            new_g[rr][k] = c
            rr -= 1
        # right column up from top of block
        rr = r - 1
        while rr >= 0 and new_g[rr][k + 1] == bg:
            new_g[rr][k + 1] = c
            rr -= 1

def apply_diagonal_up_right(new_g: tp.List[tp.List[int]], blocks: tp.List[tp.Tuple[int, int, int]], bg: int, w: int) -> None:
    for r, k, c in blocks:
        s = r + k + 1
        rr = r - 1
        while rr >= 0:
            cc = s - rr
            if not (0 <= cc < w):
                break
            if new_g[rr][cc] != bg:
                break
            new_g[rr][cc] = c
            rr -= 1

def apply_diagonal_down_left(new_g: tp.List[tp.List[int]], blocks: tp.List[tp.Tuple[int, int, int]], bg: int, h: int, w: int) -> None:
    for r, k, c in blocks:
        s = r + 1 + k
        rr = r + 2
        while rr < h:
            cc = s - rr
            if not (0 <= cc < w):
                break
            if new_g[rr][cc] != bg:
                break
            new_g[rr][cc] = c
            rr += 1

def program(g: tp.List[tp.List[int]]) -> tp.List[tp.List[int]]:
    if not g or not g[0]:
        return g
    h = len(g)
    w = len(g[0])
    bg = get_background(g)
    new_g = [row[:] for row in g]
    for _ in range(h):
        blocks = find_blocks(new_g, bg)
        apply_horizontal_bottom(new_g, blocks, bg, w)
        apply_horizontal_top(new_g, blocks, bg, w)
        apply_vertical_ups(new_g, blocks, bg)
        apply_diagonal_up_right(new_g, blocks, bg, w)
        apply_diagonal_down_left(new_g, blocks, bg, h, w)
    return new_g
```