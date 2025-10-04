```python
from typing import List, Dict

def get_background_color(g: List[List[int]]) -> int:
    if not g or not g[0]:
        return 0
    count: Dict[int, int] = {}
    h = len(g)
    w = len(g[0])
    for y in range(6, h):
        for x in range(w):
            c = g[y][x]
            if c not in [0, 5, 8]:
                count[c] = count.get(c, 0) + 1
    if not count:
        return 0
    return max(count, key=count.get)

def find_content_blocks(g: List[List[int]], bg: int) -> List[Dict[str, int]]:
    blocks: List[Dict[str, int]] = []
    h = len(g)
    w = len(g[0])
    for c in range(1, 10):
        if c == bg or c == 0 or c == 5 or c == 8:
            continue
        y_min = None
        for y in range(6, h):
            has_c = any(g[y][x] == c for x in range(w))
            if has_c:
                y_min = y
                break
        if y_min is None:
            continue
        x_min = next((x for x in range(w) if g[y_min][x] == c), None)
        if x_min is None:
            continue
        x_max = x_min
        while x_max + 1 < w and g[y_min][x_max + 1] == c:
            x_max += 1
        y_max = y_min
        while y_max + 1 < h:
            if all(g[y_max + 1][x] == c for x in range(x_min, x_max + 1)):
                y_max += 1
            else:
                break
        is_rectangle = all(
            all(g[yy][x] == c for x in range(x_min, x_max + 1))
            for yy in range(y_min, y_max + 1)
        )
        if is_rectangle and (y_max - y_min + 1) * (x_max - x_min + 1) > 4:
            blocks.append({
                'color': c,
                'x_min': x_min,
                'x_max': x_max,
                'y_min': y_min,
                'y_max': y_max
            })
    return blocks

def find_maroon_block(g: List[List[int]], bg: int) -> Dict[str, int]:
    h = len(g)
    w = len(g[0])
    for y in range(6, h):
        for x in range(w):
            if g[y][x] == 8:
                x_min = x
                while x_min > 0 and g[y][x_min - 1] == 8:
                    x_min -= 1
                x_max = x
                while x_max + 1 < w and g[y][x_max + 1] == 8:
                    x_max += 1
                y_min = y
                while y_min > 6 and all(g[y_min - 1][xx] == 8 for xx in range(x_min, x_max + 1)):
                    y_min -= 1
                y_max = y
                while y_max + 1 < h and all(g[y_max + 1][xx] == 8 for xx in range(x_min, x_max + 1)):
                    y_max += 1
                return {
                    'color': 8,
                    'x_min': x_min,
                    'x_max': x_max,
                    'y_min': y_min,
                    'y_max': y_max
                }
    return {'color': 8, 'x_min': 0, 'x_max': -1, 'y_min': 0, 'y_max': -1}

def create_output_grid(w: int, out_h: int, bg: int) -> List[List[int]]:
    return [[bg] * w for _ in range(out_h)]

def place_content_blocks(out: List[List[int]], blocks: List[Dict[str, int]], shift: int):
    out_h = len(out)
    w = len(out[0])
    for b in blocks:
        c = b['color']
        x_min = b['x_min']
        x_max = b['x_max']
        y_min = b['y_min'] - shift
        y_max = b['y_max'] - shift + 1
        y_start = max(0, y_min)
        y_end = min(out_h, y_max)
        for yy in range(y_start, y_end):
            for xx in range(max(0, x_min), min(w, x_max + 1)):
                out[yy][xx] = c

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return []
    h_in = len(g)
    w = len(g[0])
    out_h = h_in - 6
    bg = get_background_color(g)
    blocks = find_content_blocks(g, bg)
    maroon = find_maroon_block(g, bg)
    out = create_output_grid(w, out_h, bg)
    place_content_blocks(out, blocks, 6)
    x_min8 = maroon['x_min']
    x_max8 = maroon['x_max']
    if x_max8 < 0:
        return out
    y_min8_shift = maroon['y_min'] - 6
    y_max8_shift = maroon['y_max'] - 6
    conn_y_min = max(0, y_min8_shift)
    conn_y_max = min(out_h - 1, y_max8_shift)
    if conn_y_min > conn_y_max:
        return out
    # horizontal fill at conn rows
    h_start = None
    h_end = None
    for yy in range(conn_y_min, conn_y_max + 1):
        left_content_max = -1
        for x in range(x_min8 - 1, -1, -1):
            if out[yy][x] != bg:
                left_content_max = x
                break
        curr_start = left_content_max + 1 if left_content_max >= 0 else 0
        right_content_min = w
        for x in range(x_max8 + 1, w):
            if out[yy][x] != bg:
                right_content_min = x
                break
        curr_end = right_content_min - 1 if right_content_min < w else w - 1
        for x in range(curr_start, curr_end + 1):
            out[yy][x] = 8
        if h_start is None:
            h_start = curr_start
            h_end = curr_end
    if h_start is None or h_end < h_start:
        return out
    left_bar_start = h_start
    left_bar_end = min(h_start + 1, w - 1)
    right_bar_start = max(h_end - 1, 0)
    right_bar_end = h_end
    # middle bar full
    for yy in range(out_h):
        for xx in range(x_min8, x_max8 + 1):
            if out[yy][xx] == bg:
                out[yy][xx] = 8
    # left bar lower
    has_left_below = any(
        b['y_min'] < out_h and b['y_max'] > conn_y_max and b['x_min'] <= left_bar_start
        for b in blocks
    )
    if has_left_below:
        lower_start_y = conn_y_max + 1
        min_y = min((b['y_min'] for b in blocks), default=out_h)
        lower_end_y = min_y - 1
        if lower_start_y <= lower_end_y:
            for yy in range(lower_start_y, lower_end_y + 1):
                for xx in range(left_bar_start, left_bar_end + 1):
                    if out[yy][xx] == bg:
                        out[yy][xx] = 8
    # right bar upper
    has_right_above = any(
        b['y_max'] > 0 and b['y_min'] < conn_y_min and b['x_max'] >= right_bar_end
        for b in blocks
    )
    if has_right_above:
        upper_end_y = conn_y_min - 1
        if 0 <= upper_end_y:
            for yy in range(0, upper_end_y + 1):
                for xx in range(right_bar_start, right_bar_end + 1):
                    if out[yy][xx] == bg:
                        out[yy][xx] = 8
    # bottom horizontal
    min_y = min((b['y_min'] for b in blocks), default=out_h)
    gap_rows = max(0, min_y - conn_y_max - 1)
    if gap_rows > 0:
        h_bottom = 2 if gap_rows > 4 else 1
        bottom_y_start = min_y - h_bottom
        x_start_bottom = left_bar_start if has_left_below else x_min8
        lowest_blocks = [b for b in blocks if b['y_min'] == min_y]
        reaches_right = any(b['x_max'] >= right_bar_start for b in lowest_blocks)
        x_end_bottom = x_max8 if reaches_right else w - 1
        for yy in range(max(bottom_y_start, 0), min_y):
            for xx in range(x_start_bottom, x_end_bottom + 1):
                if out[yy][xx] == bg:
                    out[yy][xx] = 8
    # upper right gap fills
    right_blocks_upper = [
        b for b in blocks
        if b['x_min'] > x_max8 and b['y_min'] < conn_y_min
    ]
    if right_blocks_upper:
        right_blocks_upper.sort(key=lambda b: b['y_min'])
        for i in range(len(right_blocks_upper) - 1):
            prev = right_blocks_upper[i]
            nxt = right_blocks_upper[i + 1]
            prev_end = prev['y_max']
            next_start = nxt['y_min']
            if prev_end < next_start:
                gap_start = prev_end
                gap_h = next_start - gap_start - 1
                fill_h = prev['y_max'] - prev['y_min'] + 1
                actual_h = min(fill_h, gap_h)
                fill_start_y = gap_start
                fill_end_y = gap_start + actual_h - 1
                if fill_end_y >= conn_y_min:
                    fill_end_y = conn_y_min - 1
                if fill_start_y <= fill_end_y:
                    for yy in range(max(0, fill_start_y), min(out_h - 1, fill_end_y) + 1):
                        for xx in range(right_bar_start, w):
                            if out[yy][xx] == bg:
                                out[yy][xx] = 8
    return out
```