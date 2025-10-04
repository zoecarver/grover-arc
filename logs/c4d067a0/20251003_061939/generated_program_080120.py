```python
import typing as tp
from collections import Counter

def find_background(g: tp.List[tp.List[int]]) -> int:
    flat = [cell for row in g for cell in row]
    count = Counter(flat)
    return count.most_common(1)[0][0]

def find_min_fg(g: tp.List[tp.List[int]], bg: int) -> int:
    candidates = [c for row in g for c in row if c != bg]
    return min(candidates) if candidates else bg

def find_large_blocks(g: tp.List[tp.List[int]], bg: int) -> tp.List[tp.Dict[str, int]]:
    n = len(g)
    blocks = []
    visited = [[False] * n for _ in range(n)]
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    for y in range(n):
        for x in range(n):
            if g[y][x] != bg and not visited[y][x]:
                color = g[y][x]
                stack = [(y, x)]
                component_size = 0
                min_y, max_y = y, y
                min_x, max_x = x, x
                while stack:
                    cy, cx = stack.pop()
                    if visited[cy][cx]:
                        continue
                    visited[cy][cx] = True
                    component_size += 1
                    min_y = min(min_y, cy)
                    max_y = max(max_y, cy)
                    min_x = min(min_x, cx)
                    max_x = max(max_x, cx)
                    for dy, dx in directions:
                        ny = cy + dy
                        nx = cx + dx
                        if 0 <= ny < n and 0 <= nx < n and not visited[ny][nx] and g[ny][nx] == color:
                            stack.append((ny, nx))
                if component_size > 1:
                    w = max_x - min_x + 1
                    h = max_y - min_y + 1
                    if component_size == w * h:
                        filled = True
                        for iy in range(min_y, max_y + 1):
                            for ix in range(min_x, max_x + 1):
                                if g[iy][ix] != color:
                                    filled = False
                                    break
                            if not filled:
                                break
                        if filled:
                            blocks.append({
                                'y1': min_y,
                                'y2': max_y,
                                'x1': min_x,
                                'x2': max_x,
                                'color': color,
                                'h': h,
                                'w': w
                            })
    return blocks

def has_special(g: tp.List[tp.List[int]], bg: int, blocks: tp.List[tp.Dict[str, int]], y1: int, h: int, large_color: int, min_fg: int) -> tp.Tuple[bool, int]:
    n = len(g)
    if not blocks:
        return False, 0
    min_x1 = min(b['x1'] for b in blocks)
    for yy in range(y1, y1 + h):
        for xx in range(min_x1):
            c = g[yy][xx]
            if c != bg and c != large_color and c != min_fg:
                return True, c
    return False, 0

def calculate_normal_positions(y1: int, h: int, n: int) -> tp.List[int]:
    step = 5
    added = []
    p1 = y1 + step
    if p1 + h - 1 < n:
        added.append(p1)
        p2 = y1 + 2 * step
        if p2 + h - 1 < n:
            added.append(p2)
    if len(added) < 2:
        added = []
        p1 = y1 - step
        if p1 >= 0:
            added.append(p1)
            p2 = y1 - 2 * step
            if p2 >= 0:
                added.append(p2)
    return added

def add_rectangle(out: tp.List[tp.List[int]], py: int, x1: int, x2: int, color: int, h: int, n: int):
    for i in range(h):
        yy = py + i
        if 0 <= yy < n:
            for xx in range(x1, x2 + 1):
                out[yy][xx] = color

def program(g: tp.List[tp.List[int]]) -> tp.List[tp.List[int]]:
    n = len(g)
    out = [row[:] for row in g]
    bg = find_background(g)
    flat = [cell for row in g for cell in row]
    min_fg = find_min_fg(g, bg)
    blocks = find_large_blocks(g, bg)
    if not blocks:
        return out
    h = blocks[0]['h']
    original_y1 = blocks[0]['y1']
    center = (n - 1) // 2
    large_color = blocks[0]['color']
    has_special_flag, special_c = has_special(g, bg, blocks, original_y1, h, large_color, min_fg)
    added_pos: tp.List[int] = []
    if has_special_flag:
        step = special_c
        s_center = center
        if s_center + h - 1 >= n:
            s_center = n - h
        temp_pos = [s_center - step, s_center, s_center + step]
        added_pos = [p for p in temp_pos if 0 <= p and p + h - 1 < n]
    else:
        added_pos = calculate_normal_positions(original_y1, h, n)
    if bg == 8 or has_special_flag:
        rep_color = min_fg
        for p in added_pos:
            for block in blocks:
                add_rectangle(out, p, block['x1'], block['x2'], rep_color, h, n)
        if has_special_flag and added_pos:
            max_x1 = max(b['x1'] for b in blocks)
            add_w = blocks[0]['w']
            add_x1 = max_x1 + special_c
            add_x2 = add_x1 + add_w - 1
            for i in range(1, len(added_pos)):
                p = added_pos[i]
                add_rectangle(out, p, add_x1, add_x2, special_c, h, n)
    else:
        candidates = [c for row in g for c in row if c > min_fg and c != bg]
        next_min = min(candidates) if candidates else min_fg + 1
        if len(added_pos) == 2 and len(blocks) >= 2:
            dists = {p: abs(p - original_y1) for p in added_pos}
            farthest = max(dists, key=dists.get)
            closer = [p for p in added_pos if p != farthest][0]
            for p in added_pos:
                if p == farthest:
                    c_left = min_fg
                    c_right = next_min
                else:
                    c_left = next_min
                    c_right = next_min
                add_rectangle(out, p, blocks[0]['x1'], blocks[0]['x2'], c_left, h, n)
                add_rectangle(out, p, blocks[1]['x1'], blocks[1]['x2'], c_right, h, n)
        else:
            for p in added_pos:
                for block in blocks:
                    add_rectangle(out, p, block['x1'], block['x2'], min_fg, h, n)
    return out
```