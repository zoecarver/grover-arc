```python
from typing import List, Dict
from itertools import chain

def flatten_grid(g: List[List[int]]) -> List[int]:
    return list(chain.from_iterable(g))

def get_colors(g: List[List[int]]) -> set:
    flat = flatten_grid(g)
    return {x for x in set(flat) if x != 8}

def first_appearance_order(g: List[List[int]]) -> List[int]:
    seen = set()
    order = []
    for row in g:
        for cell in row:
            if cell != 8 and cell not in seen:
                seen.add(cell)
                order.append(cell)
    return order

def count_per_color(g: List[List[int]]) -> Dict[int, int]:
    flat = flatten_grid(g)
    counts = {}
    for cell in flat:
        if cell != 8:
            counts[cell] = counts.get(cell, 0) + 1
    return counts

def create_blank(h: int, w: int, fill: int = 8) -> List[List[int]]:
    return [[fill] * w for _ in range(h)]

def draw_h(out: List[List[int]], start_r: int, start_c: int, color: int, count: int, w: int):
    if count < 4 or color is None:
        return 0  # return full_width 0
    full_width = max(1, (count - 4) // 2)
    pixels_used = 0
    # top row: 2 pixels left aligned
    for j in range(min(2, w - start_c)):
        if pixels_used < count:
            out[start_r][start_c + j] = color
            pixels_used += 1
    # middle rows: full_width
    for dr in range(1, 3):
        rr = start_r + dr
        if rr >= len(out):
            break
        for j in range(min(full_width, w - start_c)):
            if pixels_used < count:
                out[rr][start_c + j] = color
                pixels_used += 1
    # bottom row: 2 pixels left aligned
    rr = start_r + 3
    if rr < len(out):
        for j in range(min(2, w - start_c)):
            if pixels_used < count:
                out[rr][start_c + j] = color
                pixels_used += 1
    return full_width

def draw_i(out: List[List[int]], start_r: int, start_c: int, color: int, count: int, w: int):
    if count < 2 or color is None:
        return 0  # return full_width 0
    full_width = max(1, (count - 2) // 2)
    pixels_used = 0
    # top: 1 pixel at right end
    right_pos = min(start_c + full_width - 1, w - 1)
    if start_r < len(out) and right_pos >= 0:
        out[start_r][right_pos] = color
        pixels_used += 1
    # middle rows: full_width left aligned
    for dr in range(1, 3):
        rr = start_r + dr
        if rr >= len(out):
            break
        for j in range(min(full_width, w - start_c)):
            if pixels_used < count:
                out[rr][start_c + j] = color
                pixels_used += 1
    # bottom: 1 pixel at right end
    rr = start_r + 3
    if rr < len(out) and right_pos >= 0:
        if pixels_used < count:
            out[rr][right_pos] = color
            pixels_used += 1
    return full_width

def draw_top(out: List[List[int]], start_r: int, start_c_space: int, color: int, count: int, w: int, right_h: int, left_i: int):
    if count == 0 or color is None:
        return
    # Place base 2 in main top row space
    pixels_used = 0
    rr = start_r
    for j in range(2):
        cc = start_c_space + j
        if cc < w and pixels_used < count:
            out[rr][cc] = color
            pixels_used += 1
    remaining = count - pixels_used
    if remaining <= 0:
        return
    # Add extra rows above in space cols
    num_extra = remaining // 2
    for i in range(num_extra):
        rr = start_r - 1 - i
        if rr < 0:
            break
        for j in range(2):
            cc = start_c_space + j
            if cc < w and pixels_used < count:
                out[rr][cc] = color
                pixels_used += 1
    remaining = count - pixels_used
    if remaining > 0:
        # Add one more row with placements at right_h and left_i if possible
        rr = start_r - 1 - num_extra
        if rr >= 0:
            positions = [right_h, left_i]
            for cc in positions:
                if 0 <= cc < w and pixels_used < count:
                    out[rr][cc] = color
                    pixels_used += 1
            # if still remaining, place in space
            for j in range(2):
                cc = start_c_space + j
                if cc < w and pixels_used < count:
                    out[rr][cc] = color
                    pixels_used += 1

def draw_bottom(out: List[List[int]], start_r: int, start_c_space: int, color: int, count: int, w: int):
    if count == 0 or color is None:
        return
    # Place base 2 in main bottom row space
    pixels_used = 0
    rr = start_r + 3
    if rr < len(out):
        for j in range(2):
            cc = start_c_space + j
            if cc < w and pixels_used < count:
                out[rr][cc] = color
                pixels_used += 1
    remaining = count - pixels_used
    if remaining <= 0:
        return
    # Add extra rows below in space cols
    num_extra = remaining // 2
    for i in range(num_extra):
        rr = start_r + 3 + 1 + i
        if rr >= len(out):
            break
        for j in range(2):
            cc = start_c_space + j
            if cc < w and pixels_used < count:
                out[rr][cc] = color
                pixels_used += 1
    remaining = count - pixels_used
    if remaining > 0:
        # Add one more row below with placements if needed, but simple space for now
        rr = start_r + 3 + 1 + num_extra
        if rr < len(out):
            for j in range(min(remaining, 2)):
                cc = start_c_space + j
                if cc < w:
                    out[rr][cc] = color
                    pixels_used += 1

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return []
    h = len(g)
    w = len(g[0])
    out = create_blank(h, w)
    order = first_appearance_order(g)
    counts = count_per_color(g)
    used = order[:4] + [None] * max(0, 4 - len(order))
    i_color = used[0]
    top_color = used[1]
    h_color = used[2]
    bottom_color = used[3]
    start_r = h // 2 - 2
    start_c_h = 2
    start_c_i = 8
    start_c_space = 6
    # Draw H and I first to get widths
    h_width = draw_h(out, start_r, start_c_h, h_color, counts.get(h_color, 0), w)
    i_width = draw_i(out, start_r, start_c_i, i_color, counts.get(i_color, 0), w)
    right_h = start_c_h + h_width - 1 if h_width > 0 else start_c_h + 1
    left_i = start_c_i
    # Draw top
    draw_top(out, start_r, start_c_space, top_color, counts.get(top_color, 0), w, right_h, left_i)
    # Draw bottom
    draw_bottom(out, start_r, start_c_space, bottom_color, counts.get(bottom_color, 0), w)
    return out
```