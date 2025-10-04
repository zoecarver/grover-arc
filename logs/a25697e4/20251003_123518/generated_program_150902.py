```python
from collections import Counter
from typing import List, Tuple

def get_background(g: List[List[int]]) -> int:
    if not g or not g[0]:
        return 1
    flat = [cell for row in g for cell in row]
    return Counter(flat).most_common(1)[0][0]

def copy_grid(g: List[List[int]]) -> List[List[int]]:
    return [row[:] for row in g]

def create_bg_grid(g: List[List[int]], bg: int) -> List[List[int]]:
    h = len(g)
    w = len(g[0]) if h > 0 else 0
    return [[bg] * w for _ in range(h)]

def detect_left_structure(g: List[List[int]], bg: int, main_candidate: int) -> Tuple[bool, int, int, int, int]:
    h = len(g)
    w = len(g[0]) if h > 0 else 0
    left_size = min(4, w)
    full_rows = []
    partial_rows = []
    for r in range(h):
        left_count = sum(1 for j in range(left_size) if g[r][j] == main_candidate)
        if left_count == left_size:
            full_rows.append(r)
        elif left_count == 2:
            partial_rows.append(r)
    if len(full_rows) != 2 or len(partial_rows) != 1:
        return False, 0, 0, 0, 0
    top = min(full_rows)
    bottom = max(full_rows)
    if bottom != top + 3:
        return False, 0, 0, 0, 0
    middle = partial_rows[0]
    if not (top < middle < bottom):
        return False, 0, 0, 0, 0
    gap_rows = [r for r in range(top + 1, bottom) if r != middle and sum(1 for j in range(left_size) if g[r][j] == main_candidate) == 0]
    if len(gap_rows) != 1:
        return False, 0, 0, 0, 0
    return True, top, middle, bottom, gap_rows[0]

def get_non_bg_counter(g: List[List[int]], bg: int) -> Counter:
    flat = [cell for row in g for cell in row if cell != bg]
    return Counter(flat)

def get_top_three_non_bg(non_bg_counter: Counter) -> List[int]:
    if not non_bg_counter:
        return []
    items = non_bg_counter.most_common(3)
    keys = [k for k, _ in items]
    return sorted(keys)

def get_noise_colors(non_bg_counter: Counter, main_color: int) -> Tuple[int, int]:
    other = non_bg_counter.copy()
    if main_color in other:
        del other[main_color]
    if len(other) < 2:
        return 0, 0
    items = other.most_common(2)
    n1, n2 = [k for k, _ in items]
    return min(n1, n2), max(n1, n2)

def get_upper_pattern() -> List[Tuple[int, int, int]]:
    pattern = []
    for dc in range(4):
        pattern.append((0, dc, 0))
    for dc in range(2):
        pattern.append((1, dc, 0))
    for dc in range(2, 4):
        pattern.append((1, dc, 2))
    for dc in range(4, 9):
        pattern.append((1, dc, 1))
    for dc in range(4):
        pattern.append((2, dc, 2))
    pattern.append((2, 8, 1))
    for dc in range(4):
        pattern.append((3, dc, 0))
    for dc in range(8, 10):
        pattern.append((3, dc, 1))
    return pattern

def get_lower_pattern() -> List[Tuple[int, int, int]]:
    pattern = []
    for dc in range(4):
        pattern.append((0, dc, 0))
    for dc in range(8, 10):
        pattern.append((0, dc, 2))
    for dc in range(4):
        pattern.append((1, dc, 1))
    pattern.append((1, 8, 2))
    for dc in range(2):
        pattern.append((2, dc, 0))
    for dc in range(2, 4):
        pattern.append((2, dc, 1))
    for dc in range(4, 9):
        pattern.append((2, dc, 2))
    for dc in range(4):
        pattern.append((3, dc, 0))
    return pattern

def place_letter_pattern(out: List[List[int]], top: int, main_color: int, inner: int, outer: int, is_upper: bool, h: int, w: int) -> None:
    if is_upper:
        pattern = get_upper_pattern()
    else:
        pattern = get_lower_pattern()
    col_map = [main_color, inner, outer]
    for dr, dc, wh in pattern:
        r = top + dr
        c = dc
        if 0 <= r < h and 0 <= c < w:
            out[r][c] = col_map[wh]

def place_triangle(out: List[List[int]], start_r: int, start_c: int, color: int, h: int, w: int) -> None:
    positions = [
        (start_r + 0, start_c + 1),
        (start_r + 1, start_c + 0),
        (start_r + 1, start_c + 1),
        (start_r + 2, start_c + 1),
        (start_r + 2, start_c + 2),
        (start_r + 2, start_c + 3)
    ]
    for r, c in positions:
        if 0 <= r < h and 0 <= c < w:
            out[r][c] = color

def place_butterfly(out: List[List[int]], start_r: int, start_c: int, frame: int, fill: int, h: int, w: int) -> None:
    for dr in range(3):
        r = start_r + dr
        if r >= h:
            continue
        if dr == 0:
            cs = [0, 1, 2, 3, 4]
            cols = [frame, fill, fill, fill, frame]
        else:
            cs = [0, 1, 2, 3, 4]
            cols = [frame, fill, frame, frame, frame]
        for ddc, col in zip(cs, cols):
            c = start_c + ddc
            if 0 <= c < w:
                out[r][c] = col

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return g
    h = len(g)
    w = len(g[0])
    bg = get_background(g)
    out = create_bg_grid(g, bg)
    non_bg_counter = get_non_bg_counter(g, bg)
    if not non_bg_counter:
        return out
    possible_mains = [k for k in non_bg_counter if non_bg_counter[k] > 0]
    structure_found = False
    top = middle = bottom = gap_r = 0
    main_color = 0
    for cand in sorted(possible_mains):
        has, t, m, b, g = detect_left_structure(g, bg, cand)
        if has:
            structure_found = True
            top = t
            middle = m
            bottom = b
            gap_r = g
            main_color = cand
            break
    if structure_found:
        inner, outer = get_noise_colors(non_bg_counter, main_color)
        if inner == 0 or outer == 0:
            return copy_grid(g)
        is_upper = (middle == top + 1)
        place_letter_pattern(out, top, main_color, inner, outer, is_upper, h, w)
    else:
        top_three = get_top_three_non_bg(non_bg_counter)
        if len(top_three) < 3:
            return copy_grid(g)
        low, mid, high = sorted(top_three)
        start_r = h - 6
        tri_c = 9
        place_triangle(out, start_r, tri_c, low, h, w)
        butter_r = start_r + 3
        butter_c = 11
        place_butterfly(out, butter_r, butter_c, mid, high, h, w)
    return out
```