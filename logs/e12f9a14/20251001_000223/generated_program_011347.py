```python
import typing as tp
from collections import Counter

def get_background(g: tp.List[tp.List[int]]) -> int:
    """Identify the background color as the most frequent value in the grid."""
    if not g or not g[0]:
        return 0
    flat = [cell for row in g for cell in row]
    return Counter(flat).most_common(1)[0][0]

def find_blocks(g: tp.List[tp.List[int]], bg: int) -> tp.List[tp.Tuple[int, int, int]]:
    """Find all 2x2 blocks of identical color c where c != bg and c != 3, returning sorted list of (row, col, c)."""
    blocks = []
    h = len(g)
    w = len(g[0]) if h > 0 else 0
    for r in range(h - 1):
        for k in range(w - 1):
            c = g[r][k]
            if c != bg and c != 3 and g[r][k + 1] == c and g[r + 1][k] == c and g[r + 1][k + 1] == c:
                blocks.append((r, k, c))
    return sorted(blocks, key=lambda x: (x[0], x[1]))

def apply_horizontal(new_g: tp.List[tp.List[int]], r: int, k: int, c: int, bg: int, w: int) -> bool:
    """Propagate color c horizontally left and right on both rows r and r+1 of the block, filling background cells until blocked."""
    changed = False
    for rr in [r, r + 1]:
        # left
        cc = k - 1
        while cc >= 0 and new_g[rr][cc] == bg:
            new_g[rr][cc] = c
            changed = True
            cc -= 1
        # right
        cc = k + 2
        while cc < w and new_g[rr][cc] == bg:
            new_g[rr][cc] = c
            changed = True
            cc += 1
    return changed

def apply_vertical(new_g: tp.List[tp.List[int]], r: int, k: int, c: int, bg: int, h: int) -> bool:
    """Propagate color c vertically up and down on both columns k and k+1 of the block, filling background cells until blocked."""
    changed = False
    for col in [k, k + 1]:
        # up
        rr = r - 1
        while rr >= 0 and new_g[rr][col] == bg:
            new_g[rr][col] = c
            changed = True
            rr -= 1
        # down
        rr = r + 2
        while rr < h and new_g[rr][col] == bg:
            new_g[rr][col] = c
            changed = True
            rr += 1
    return changed

def apply_up_right(new_g: tp.List[tp.List[int]], r: int, k: int, c: int, bg: int, h: int, w: int) -> bool:
    """Propagate color c up-right from adjacent to top-right corner of the block, filling background cells until blocked."""
    changed = False
    rr = r - 1
    cc = k + 2
    while rr >= 0 and cc < w and new_g[rr][cc] == bg:
        new_g[rr][cc] = c
        changed = True
        rr -= 1
        cc += 1
    return changed

def apply_up_left(new_g: tp.List[tp.List[int]], r: int, k: int, c: int, bg: int, h: int, w: int) -> bool:
    """Propagate color c up-left from adjacent to top-left corner of the block, filling background cells until blocked."""
    changed = False
    rr = r - 1
    cc = k - 1
    while rr >= 0 and cc >= 0 and new_g[rr][cc] == bg:
        new_g[rr][cc] = c
        changed = True
        rr -= 1
        cc -= 1
    return changed

def apply_down_right(new_g: tp.List[tp.List[int]], r: int, k: int, c: int, bg: int, h: int, w: int) -> bool:
    """Propagate color c down-right from adjacent to bottom-right corner of the block, filling background cells until blocked."""
    changed = False
    rr = r + 2
    cc = k + 2
    while rr < h and cc < w and new_g[rr][cc] == bg:
        new_g[rr][cc] = c
        changed = True
        rr += 1
        cc += 1
    return changed

def apply_down_left(new_g: tp.List[tp.List[int]], r: int, k: int, c: int, bg: int, h: int, w: int) -> bool:
    """Propagate color c down-left from adjacent to bottom-left corner of the block, filling background cells until blocked."""
    changed = False
    rr = r + 2
    cc = k - 1
    while rr < h and cc >= 0 and new_g[rr][cc] == bg:
        new_g[rr][cc] = c
        changed = True
        rr += 1
        cc -= 1
    return changed

def program(g: tp.List[tp.List[int]]) -> tp.List[tp.List[int]]:
    """Main function: iteratively propagate from 2x2 blocks until no changes occur, composing all expansion rules."""
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
        for r, k, c in blocks:
            if apply_horizontal(new_g, r, k, c, bg, w):
                changed = True
            if apply_vertical(new_g, r, k, c, bg, h):
                changed = True
            if apply_up_right(new_g, r, k, c, bg, h, w):
                changed = True
            if apply_up_left(new_g, r, k, c, bg, h, w):
                changed = True
            if apply_down_right(new_g, r, k, c, bg, h, w):
                changed = True
            if apply_down_left(new_g, r, k, c, bg, h, w):
                changed = True
        if not changed:
            break
    return new_g
```